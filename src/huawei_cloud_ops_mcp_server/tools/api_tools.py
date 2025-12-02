import json
from typing import Optional, Dict

from huawei_cloud_ops_mcp_server.huaweicloud.config import base_url
from huawei_cloud_ops_mcp_server.common.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.utils import (
    HuaweiCloudClient
)
from huawei_cloud_ops_mcp_server.config.logger import logger


class HuaweiApiCloudTools:
    tool_metadatas = {
        'huawei_api_request': ToolMetadata(
            priority=5,
            category='api_request',
            timeout=30,
            retryable=True,
        ),
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
                raise ValueError(f'错误: 当前仅支持GET请求方式, 不支持 "{method}"。')

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
