import json
from pathlib import Path
from typing import Dict, Optional

from tinydb import TinyDB, Query

from huawei_cloud_ops_mcp_server.common.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
    PRICE_DBS
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
    }

    @staticmethod
    def _get_db_path(service: str) -> Optional[Path]:
        """获取指定服务的数据库路径"""
        if service not in PRICE_DBS:
            return None
        db_path = Path(PRICE_DBS[service])
        if not db_path.exists():
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
        service: str = 'ecs',
        filters: Optional[Dict[str, str]] = None,
        data_filters: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 50
    ) -> str:
        """查询价格信息

        Args:
            service: 服务名称 (如: ecs, rds, evs 等)
            filters: 查询条件字典 (可选,支持模糊匹配)
            data_filters: price_table.data 的过滤条件 (可选,支持模糊匹配)
            page: 页码, 从1开始 (默认: 1)
            page_size: 每页记录数 (默认: 50)

        Returns:
            str: 查询结果 (JSON 格式字符串)

        """
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
        try:
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
                raise ValueError('未查询到价格')
        finally:
            # 确保数据库连接被关闭
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

        # 分页处理
        total_count = len(raw_results)
        if page_size > 0:
            total_pages = (total_count + page_size - 1) // page_size
        else:
            total_pages = 1

        # 验证页码有效性
        if page < 1:
            page = 1
        elif page > total_pages and total_pages > 0:
            page = total_pages

        # 计算分页切片
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_results = raw_results[start_index:end_index]

        # 返回 JSON 结果
        response = {
            'service': service,
            'filters': filters,
            'data_filters': data_filters,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'count': len(paginated_results),
            'results': paginated_results
        }

        logger.info(
            f'价格查询成功: service={service}, '
            f'找到 {total_count} 条记录, '
            f'第 {page}/{total_pages} 页, '
            f'本页 {len(paginated_results)} 条'
        )
        price_json = json.dumps(
            response, separators=(',', ':'),
            ensure_ascii=False
        )
        return price_json
