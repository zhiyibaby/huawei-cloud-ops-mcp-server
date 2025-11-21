import json
from pathlib import Path
from typing import Dict, Optional

from tinydb import TinyDB, Query

from huawei_cloud_ops_mcp_server.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import PRICE_DOCS
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
        if service not in PRICE_DOCS:
            return None
        db_path = Path(PRICE_DOCS[service])
        if not db_path.exists():
            logger.warning(f'价格数据库文件不存在: {db_path}')
            return None
        return db_path

    @staticmethod
    @strict_error_handler
    async def query_price(
        service: str,
        filters: Optional[Dict[str, str]] = None
    ) -> str:
        """查询价格信息

        Args:
            service: 服务名称 (如: ecs, rds, evs 等)
            filters: 查询条件字典 (可选,支持模糊匹配)
                支持的字段: region, zone, cpu_arch, spec1, spec2, image
                例如: {'region': '华北-北京四', 'spec2': 'Ac9s', 'image': 'Windows'}

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
                available_services = ', '.join(sorted(PRICE_DOCS.keys()))
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

            if not raw_results:
                db.close()
                raise ValueError('未查询到价格')

            db.close()

            # 返回 JSON 结果
            response = {
                'service': service,
                'filters': filters,
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
