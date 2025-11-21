import json
from pathlib import Path
from typing import Dict, Optional

from tinydb import TinyDB, Query

from huawei_cloud_ops_mcp_server.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
    PRICE_DBS, PRICE_DOCS
)
from huawei_cloud_ops_mcp_server.logger import logger


class HuaweiPriceTools:
    tool_metadatas = {
        'query_price': ToolMetadata(
            priority=5,
            category='price_query',
            timeout=30,
            retryable=True
        ),
        'get_price_structure_doc': ToolMetadata(
            priority=3,
            category='price_documentation',
            timeout=10,
            retryable=False
        ),
    }

    @staticmethod
    def _get_db_path(service: str) -> Optional[Path]:
        """获取指定服务的数据库路径"""
        if service not in PRICE_DBS:
            return None
        db_path = Path(PRICE_DBS[service])
        if not db_path.exists():
            logger.warning(f'价格数据库文件不存在: {db_path}')
            return None
        return db_path

    @staticmethod
    def _filter_price_table_data(
        price_table: Dict,
        data_filters: Dict[str, str]
    ) -> Dict:
        """根据 data_filters 过滤 price_table.data 中的内容

        Args:
            price_table: 价格表对象，包含 headers 和 data
            data_filters: 过滤条件字典
                支持两种方式：
                1. 按列名（表头）: {'规格名称': 'ac9s.large.2', '核数': '2核'}
                2. 按列索引: {'0': 'ac9s', '1': '2核'} (索引从0开始)
                3. 混合使用: {'规格名称': 'ac9s', '1': '4GiB'}

        Returns:
            过滤后的 price_table 对象
        """
        if not price_table or 'data' not in price_table:
            return price_table

        headers = price_table.get('headers', [])
        data = price_table.get('data', [])

        if not data_filters or not data:
            return price_table

        # 构建列名到索引的映射
        header_to_index = {header: idx for idx, header in enumerate(headers)}

        # 过滤数据行
        filtered_data = []
        for row in data:
            match = True
            for filter_key, filter_value in data_filters.items():
                if not filter_value:
                    continue

                # 确定列索引
                if filter_key.isdigit():
                    # 按索引查询
                    col_index = int(filter_key)
                elif filter_key in header_to_index:
                    # 按列名查询
                    col_index = header_to_index[filter_key]
                else:
                    # 列名或索引无效，跳过此过滤条件
                    logger.warning(
                        f'无效的过滤字段: {filter_key},'
                        f'可用列名: {headers},'
                        f'索引范围: 0-{len(headers)-1}'
                    )
                    continue

                # 检查列索引是否有效
                if col_index >= len(row):
                    match = False
                    break

                # 模糊匹配
                cell_value = str(row[col_index]) if row[col_index] else ''
                if filter_value not in cell_value:
                    match = False
                    break

            if match:
                filtered_data.append(row)

        # 返回过滤后的结果
        return {
            'headers': headers,
            'data': filtered_data
        }

    @staticmethod
    @strict_error_handler
    async def query_price(
        service: str,
        filters: Optional[Dict[str, str]] = None,
        data_filters: Optional[Dict[str, str]] = None
    ) -> str:
        """查询价格信息

        Args:
            service: 服务名称 (如: ecs, rds, evs 等)
            filters: 查询条件字典 (可选,支持模糊匹配)
                支持的字段: region, zone, cpu_arch, spec1, spec2, image
                例如: {'region': '华北-北京四', 'spec2': 'Ac9s', 'image': 'Windows'}
            data_filters: price_table.data 的过滤条件 (可选,支持模糊匹配)
                支持两种方式：
                1. 按列名（表头）: {'规格名称': 'ac9s.large.2', '核数': '2核',
                   '内存': '4GiB'}
                2. 按列索引: {'0': 'ac9s', '1': '2核'}
                   (索引从0开始，对应headers的顺序)
                3. 混合使用: {'规格名称': 'ac9s', '1': '4GiB'}
                例如: {'规格名称': 'large', '核数': '2核'} 会匹配所有规格名称
                包含'large'且核数为'2核'的行

        Returns:
            str: 查询结果 (JSON 格式字符串)

        示例:
            # 查询所有 ECS 价格
            query_price(service='ecs')

            # 按区域查询
            query_price(service='ecs', filters={'region': '华北-北京四'})

            # 多条件查询
            query_price(
                service='ecs',
                filters={'region': '华北-北京四', 'spec2': 'Ac9s'}
            )

            # 查询并过滤 price_table.data 中的内容
            query_price(
                service='ecs',
                filters={'region': '华北-北京四'},
                data_filters={'规格名称': 'large', '核数': '2核'}
            )

            # 按列索引过滤
            query_price(
                service='ecs',
                # 规格名称包含'ac9s'且内存为'4GiB'
                data_filters={'0': 'ac9s', '2': '4GiB'}
            )
        """
        try:
            filters = filters or {}

            # 区域映射：如果查询北京一，自动查询北京四
            if filters.get('region') and '北京一' in filters['region']:
                original_region = filters['region']
                filters['region'] = filters['region'].replace('北京一', '北京四')
                logger.info(
                    f'区域映射: "{original_region}" -> "{filters["region"]}"'
                )

            logger.info(
                f'查询价格: service={service}, filters={filters}'
            )

            db_path = HuaweiPriceTools._get_db_path(service)
            if not db_path:
                available_services = ', '.join(sorted(PRICE_DBS.keys()))
                raise ValueError(
                    f'服务 "{service}" 不可用或数据库文件不存在。'
                    f'可用服务: {available_services}'
                )

            db = TinyDB(str(db_path), encoding='utf-8')
            price_query = Query()

            # 根据 filters 动态生成查询条件
            conditions = []
            for field, value in filters.items():
                if value:
                    # 支持 spec 字段同时匹配 spec1 和 spec2
                    if field == 'spec':
                        conditions.append(
                            (price_query.spec1.search(value)) |
                            (price_query.spec2.search(value))
                        )
                    else:
                        # 使用 getattr 动态获取字段查询对象
                        field_query = getattr(price_query, field, None)
                        if field_query:
                            conditions.append(field_query.search(value))

            if conditions:
                query = conditions[0]
                for condition in conditions[1:]:
                    query = query & condition
                raw_results = db.search(query)
            else:
                # 如果没有查询条件，返回所有记录
                raw_results = db.all()

            if not raw_results:
                db.close()
                raise ValueError('未查询到价格')

            db.close()

            # 如果指定了 data_filters，对每个结果的 price_table.data 进行过滤
            if data_filters:
                filtered_results = []
                for result in raw_results:
                    if 'price_table' in result:
                        filtered_price_table = (
                            HuaweiPriceTools._filter_price_table_data(
                                result['price_table'],
                                data_filters
                            )
                        )
                        # 如果过滤后还有数据，则保留该记录
                        if filtered_price_table.get('data'):
                            result_copy = result.copy()
                            result_copy['price_table'] = filtered_price_table
                            filtered_results.append(result_copy)
                    else:
                        # 如果没有 price_table，保留原记录
                        filtered_results.append(result)

                raw_results = filtered_results

                if not raw_results:
                    raise ValueError(
                        f'未查询到符合 data_filters={data_filters} 的价格数据'
                    )

            # 返回 JSON 结果
            response = {
                'service': service,
                'filters': filters,
                'data_filters': data_filters,
                'count': len(raw_results),
                'results': raw_results
            }

            logger.info(
                f'价格查询成功: service={service}, '
                f'找到 {len(raw_results)} 条记录'
            )
            return json.dumps(response, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(
                f'价格查询失败: service={service}, 错误: {str(e)}',
                exc_info=True
            )
            raise ValueError(f'价格查询错误: {str(e)}')

    @staticmethod
    @strict_error_handler
    async def get_price_structure_doc(
        service: Optional[str] = None
    ) -> str:
        """获取价格数据结构文档说明

        Args:
            service: 服务名称 (如: ecs, rds, evs 等)，可选
                如果不提供，将返回所有可用服务的列表

        Returns:
            str: 价格数据结构文档说明 (Markdown 格式)
                如果未指定服务，返回可用服务列表

        示例:
            # 获取所有可用服务的列表
            get_price_structure_doc()

            # 获取 ECS 服务的价格数据结构文档
            get_price_structure_doc(service='ecs')

            # 获取 RDS 服务的价格数据结构文档
            get_price_structure_doc(service='rds')
        """
        try:
            if not service:
                # 返回所有可用服务的列表
                available_services = sorted(PRICE_DOCS.keys())
                if not available_services:
                    return '当前没有可用的价格数据结构文档。'

                doc = '# 可用价格数据结构文档\n\n'
                doc += '以下服务提供了价格数据结构说明文档：\n\n'
                for svc in available_services:
                    doc += (
                        f'- **{svc.upper()}**: '
                        f'使用 `get_price_structure_doc(service="{svc}")` '
                        f'获取详细文档\n'
                    )
                doc += '\n'
                doc += '## 使用说明\n\n'
                doc += (
                    '调用 `get_price_structure_doc(service="服务名称")` '
                    '可以获取指定服务的详细价格数据结构说明，'
                    '包括字段说明、数据格式、查询方式等信息。\n'
                )

                logger.info(f'返回可用服务列表: {available_services}')
                return doc

            service_lower = service.lower()

            if service_lower not in PRICE_DOCS:
                available_services = ', '.join(sorted(PRICE_DOCS.keys()))
                raise ValueError(
                    f'服务 "{service}" 没有可用的价格数据结构文档。'
                    f'可用服务: {available_services}'
                )

            doc_content = PRICE_DOCS[service_lower]

            logger.info(
                f'获取价格数据结构文档: service={service}'
            )
            return doc_content

        except Exception as e:
            logger.error(
                f'获取价格数据结构文档失败: service={service}, 错误: {str(e)}',
                exc_info=True
            )
            raise ValueError(f'获取价格数据结构文档错误: {str(e)}')
