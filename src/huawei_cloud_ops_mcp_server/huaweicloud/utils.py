import json
from urllib.parse import urlencode

from typing import Optional, Dict, Any, Tuple
from fastmcp.server.dependencies import get_http_request

from huawei_cloud_ops_mcp_server.config import (
    HUAWEI_CLOUD_ACCESS_KEY, HUAWEI_CLOUD_SECRET_KEY
)
from huawei_cloud_ops_mcp_server.utils import http_request
from huawei_cloud_ops_mcp_server.huaweicloud.apig_sdk import signer
from huawei_cloud_ops_mcp_server.logger import logger


class HuaweiCloudClient:
    """华为云统一 API 客户端"""

    def _sign_request(
        self, method: str, endpoint: str, headers: dict, body: str = ''
    ) -> dict:
        """生成华为云 API 签名"""
        try:
            sig = signer.Signer()
            sig.Key = HUAWEI_CLOUD_ACCESS_KEY
            sig.Secret = HUAWEI_CLOUD_SECRET_KEY
            r = signer.HttpRequest(method, endpoint, headers, body)
            sig.Sign(r)
            return r.headers
        except Exception as e:
            logger.error(f'生成华为云 API 签名时发生错误: {str(e)}', exc_info=True)
            raise RuntimeError(f'生成华为云 API 签名时发生错误: {str(e)}')

    def _get_request_headers(self) -> Optional[Tuple[str, str, str]]:
        """从 HTTP 请求头获取认证信息

        Returns:
            Optional[Tuple[str, str, str]]:(Host, X-Sdk-Date, Authorization)
                如果获取失败或信息不完整,返回 None
        """
        try:
            request = get_http_request()
            if not hasattr(request, 'headers'):
                return None

            request_headers = request.headers
            host = request_headers.get('Host')
            x_sdk_date = request_headers.get('X-Sdk-Date')
            authorization = request_headers.get('Authorization')

            if host and x_sdk_date and authorization:
                return (host, x_sdk_date, authorization)
        except Exception:
            pass

        return None

    def _build_endpoint_with_params(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> str:
        """构建包含查询参数的 endpoin(用于签名)"""
        if not params:
            return endpoint

        query_string = urlencode(params, doseq=True)
        separator = '&' if '?' in endpoint else '?'
        return f'{endpoint}{separator}{query_string}'

    async def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """发送请求到华为云 API(使用华为云签名)"""
        logger.info(f'发送华为云 API 请求: {method} {endpoint}')

        headers = {}

        # 尝试从请求头获取认证信息
        auth_info = self._get_request_headers()
        if auth_info:
            host, x_sdk_date, authorization = auth_info
            headers.update({
                'Host': host,
                'X-Sdk-Date': x_sdk_date,
                'Authorization': authorization
            })
        else:
            endpoint_with_params = self._build_endpoint_with_params(
                endpoint, params
            )
            body = json.dumps(data, separators=(',', ':')) if data else ''
            headers = self._sign_request(
                method, endpoint_with_params, headers, body
            )

        response = await http_request(
            method=method,
            url=endpoint,
            data=body,
            params=params,
            headers=headers,
            timeout=30
        )

        logger.info(
            f'华为云 API 请求完成: {method} {endpoint}, '
            f'状态码: {response.get("status_code")}'
        )
        return response
