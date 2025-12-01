import json
from typing import Optional, Dict

from huawei_cloud_ops_mcp_server.huaweicloud.config import base_url
from huawei_cloud_ops_mcp_server.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.utils import HuaweiCloudClient
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import API_DOCS
from huawei_cloud_ops_mcp_server.logger import logger


class HuaweiApiCloudTools:
    tool_metadatas = {
        'huawei_api_request': ToolMetadata(
            priority=5,
            category='api_request',
            timeout=30,
            retryable=True,
        ),
        'get_huawei_api_docs': ToolMetadata(
            priority=3,
            category='documentation',
            timeout=10,
            retryable=False,
        )
    }

    @staticmethod
    @strict_error_handler
    async def huawei_api_request(
        account: str,
        service: str,
        action: str,
        method: str = 'GET',
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        zone: str = '华北-北京一'
    ) -> str:
        """执行 API 请求

        Args:
            account: 账号名称(如xiaohei2018,krsk2021)
            service: 服务类型 (ecs, vpc, rds, evs, elb, ims, ces)
            action: API 动作/端点路径，如 'v1/{project_id}/cloudservers/detail'
            method: HTTP 方法
            data: 请求体数据 (用于 POST/PUT 请求)
            params: 查询参数字典，用于 GET 请求的 URL 参数
                    例如: {'name': 'test', 'status': 'ACTIVE', 'limit': 50}
                    支持多个值: {'tags': ['key1=value1', 'key2=value2']}
            zone: 区域名称，用于确定 project_id,如 '华北-北京一'

        Returns:
            str: API 响应结果 (JSON 格式字符串)
        """
        try:
            logger.info(
                f'执行华为云 API 请求: service={service}, action={action}, '
                f'method={method}, zone={zone}'
            )

            # 只允许GET请求
            if method.upper() != 'GET':
                # TODO 允许特例：LTS 日志内容查询，后续删除
                allow_post_lts_query = (
                    method.upper() == 'POST' and
                    service == 'lts' and
                    action.endswith('/content/query')
                )
                if not allow_post_lts_query:
                    raise ValueError(f'错误: 当前仅支持GET请求方式, 不支持 \"{method}\"。')

            project_id, region, url = base_url(account, service, zone)
            client = HuaweiCloudClient(identifier=account)

            if '{project_id}' in action:
                action = action.format(project_id=project_id)

            endpoint = f'{url}/{action.lstrip("/")}'

            response = await client.request(
                method.upper(), endpoint, data, params
            )

            logger.info(
                f'华为云 API 请求成功: service={service}, action={action}'
            )
            api_json = json.dumps(
                response,
                separators=(',', ':'),
                ensure_ascii=False
            )
            return api_json

        except Exception as e:
            logger.error(
                f'华为云 API 请求失败: service={service}, action={action}, '
                f'错误: {str(e)}',
                exc_info=True
            )
            raise ValueError(
                f'API 请求错误: {str(e)}'
            )

    @staticmethod
    @strict_error_handler
    async def get_huawei_api_docs(service: str = None) -> str:
        """获取华为云 API 文档说明

        Args:
            service: 服务名称 (ecs, vpc, rds, evs, elb, ims, ces)
            如果未提供，则默认返回所有文档

        Returns:
            str: API 文档说明
        """
        docs = API_DOCS
        # 若未提供服务名，默认列出所有文档
        if not service or service.lower() == 'all':
            return '\n\n'.join(
                f'=== {k.upper()} ===\n{v}'
                for k, v in docs.items()
            ).strip()
        # 有指定服务时，返回该服务文档
        if service in docs:
            # 返回内容进行压缩（移除多余换行与首尾空白）
            return ''.join(line.strip() for line in docs[service].splitlines())
        else:
            raise ValueError(f'未知服务: {service}。可用服务: {", ".join(docs.keys())}')
