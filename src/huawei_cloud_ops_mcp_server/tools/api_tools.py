import json
import asyncio
from typing import Optional, Dict

from huawei_cloud_ops_mcp_server.huaweicloud.config import base_url
from huawei_cloud_ops_mcp_server.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.huaweicloud.utils import HuaweiCloudClient
from huawei_cloud_ops_mcp_server.huaweicloud.static import (
    prompt_understanding_docs, api_operations_docs)
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import API_DOCS
from huawei_cloud_ops_mcp_server.logger import logger


class HuaweiApiCloudTools:
    tool_metadatas = {
        'prompt_understanding': ToolMetadata(
            priority=1,
            category='documentation',
            timeout=10,
            retryable=False
        ),
        'huawei_api_request': ToolMetadata(
            priority=5,
            category='api_request',
            timeout=30,
            retryable=True
        ),
        'get_huawei_api_docs': ToolMetadata(
            priority=3,
            category='documentation',
            timeout=10,
            retryable=False
        ),
        'list_common_operations': ToolMetadata(
            priority=2,
            category='documentation',
            timeout=10,
            retryable=False
        ),
    }

    @staticmethod
    async def prompt_understanding() -> str:
        """获取工具使用说明

        Returns:
            str: 工具使用说明
        """
        logger.debug('调用工具: prompt_understanding')
        return prompt_understanding_docs

    @staticmethod
    @strict_error_handler
    async def huawei_api_request(
        service: str,
        action: str,
        method: str = 'GET',
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        zone: str = '华北-北京一'
    ) -> str:
        """执行 API 请求

        Args:
            service: 服务类型 (ecs, vpc, rds, evs, elb, ims)
            action: API 动作/端点路径，如 'v1/{project_id}/cloudservers/detail'
            method: HTTP 方法，当前仅支持 GET
            data: 请求体数据 (用于 POST/PUT 请求)
            params: 查询参数字典，用于 GET 请求的 URL 参数
                    例如: {'name': 'test', 'status': 'ACTIVE', 'limit': 50}
                    支持多个值: {'tags': ['key1=value1', 'key2=value2']}
            zone: 区域名称，用于确定 project_id,如 '华北-北京一'

        Returns:
            str: API 响应结果 (JSON 格式字符串)

        示例:
            # 查询所有 ECS 实例
            huawei_api_request(
                service='ecs',
                action='v1/{project_id}/cloudservers/detail'
            )

            # 按名称和状态查询
            huawei_api_request(
                service='ecs',
                action='v1/{project_id}/cloudservers/detail',
                params={'name': 'test', 'status': 'ACTIVE', 'limit': 50}
            )
        """
        try:
            logger.info(
                f'执行华为云 API 请求: service={service}, action={action}, '
                f'method={method}, zone={zone}'
            )

            # 只允许GET请求
            if method.upper() != 'GET':
                logger.warning(f'不支持的请求方法: {method}')
                raise ValueError(f'错误: 当前仅支持GET请求方式, 不支持 "{method}"。')

            client = HuaweiCloudClient()
            project_id, region, url = base_url(service, zone)
            logger.debug(
                f'解析区域信息: zone={zone}, '
                f'project_id={project_id}, region={region}'
            )

            if '{project_id}' in action:
                action = action.format(project_id=project_id)
                logger.debug(f'替换 project_id 占位符: {action}')

            endpoint = f'{url}/{action.lstrip("/")}'
            logger.debug(f'构建的端点: {endpoint}')

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.request(method.upper(), endpoint, data, params)
            )

            logger.info(f'华为云 API 请求成功: service={service}, action={action}')
            return json.dumps(response, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(
                f'华为云 API 请求失败: service={service}, action={action}, 错误: {str(e)}',
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
            service: 服务名称 (ecs, vpc, rds, evs, elb, ims)
            如果未提供，则默认返回所有文档

        Returns:
            str: API 文档说明
        """
        logger.debug(f'调用工具: get_huawei_api_docs, service={service}')
        docs = API_DOCS
        # 若未提供服务名，默认列出所有文档
        if not service or service.lower() == 'all':
            logger.debug('返回所有服务的 API 文档')
            return '\n\n'.join(
                f'=== {k.upper()} ===\n{v}'
                for k, v in docs.items()
            ).strip()
        # 有指定服务时，返回该服务文档
        if service in docs:
            logger.debug(f'返回服务 {service} 的 API 文档')
            return docs[service]
        else:
            logger.warning(f'未知服务: {service}，可用服务: {", ".join(docs.keys())}')
            raise ValueError(f'未知服务: {service}。可用服务: {", ".join(docs.keys())}')

    @staticmethod
    async def list_common_operations() -> str:
        """获取常用操作示例

        Returns:
            str: 常用操作示例
        """
        logger.debug('调用工具: list_common_operations')
        return api_operations_docs
