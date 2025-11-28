import json
import httpx
from typing import Optional, Dict, Any
from dataclasses import dataclass

from huawei_cloud_ops_mcp_server.logger import logger


@dataclass
class ToolMetadata:
    # TODO timeout和retryable功能未实现，仅仅做标记
    priority: int  # 1-10, 1为最高优先级
    category: str  # 工具分类
    timeout: int   # 超时时间
    retryable: bool  # 是否可重试


def strict_error_handler(func):
    """
    用于函数的严格错误处理装饰器。
    捕获所有异常并返回统一结构体，不重试、不降级。

    返回结构示例:
    {
        "content": [
            {"type": "text", "text": str},
            {"type": "error_detail", "text": str}
        ],
        "isError": True,
        "errorType": str
    }
    """

    import functools
    import traceback
    import inspect

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = getattr(func, '__name__', repr(func))
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            return result
        except Exception as e:
            err_text = f'工具执行失败: {e}'
            tb = traceback.format_exc()
            logger.error(f'工具函数 {func_name} 执行失败: {e}', exc_info=True)
            return {
                'content': [
                    {'type': 'text', 'text': err_text},
                    {'type': 'error_detail', 'text': tb}
                ],
                'isError': True,
                'errorType': e.__class__.__name__,
            }
    return wrapper


async def http_request(
    method: str,
    url: str,
    data: str = None,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    通用的异步 HTTP 请求函数

    Args:
        method: HTTP 方法 (GET, POST, PUT, DELETE, PATCH 等)
        url: 请求的 URL
        data: 请求体数据(字典格式,会被序列化为 JSON)
        params: URL 查询参数字典
        headers: 自定义请求头字典(可选)
        timeout: 请求超时时间(秒),默认 30
        json_data: 直接传递的 JSON 数据
            (如果提供,将优先使用此参数而不是 data)

    Returns:
        Dict[str, Any]: 包含 status_code 和 data 的字典
        {
            'status_code': int,
            'data': dict 或 {'text': str}
        }

    示例:
        # GET 请求
        response = await http_request(
            'GET', 'https://api.example.com/users', params={'page': 1}
        )

        # POST 请求
        response = await http_request(
            'POST', 'https://api.example.com/users',
            data={'name': 'John', 'age': 30}
        )

        # 带自定义请求头
        response = await http_request(
            'GET', 'https://api.example.com/data',
            headers={'Authorization': 'Bearer token'}
        )
    """
    # 设置默认请求头
    request_headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    if headers:
        request_headers.update(headers)

    # 发送请求
    timeout_obj = httpx.Timeout(timeout, connect=timeout)
    try:
        async with httpx.AsyncClient(timeout=timeout_obj) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                params=params,
                content=data
            )

            # 解析响应
            try:
                result = response.json()
            except json.JSONDecodeError:
                result = {'text': response.text}

            if response.status_code >= 400:
                logger.warning(
                    f'HTTP 请求返回错误状态码: {response.status_code}, 响应: {result}'
                )
            return {
                'status_code': response.status_code,
                'data': result
            }
    except httpx.TimeoutException:
        logger.error(f'HTTP 请求超时: {method.upper()} {url} (超时时间: {timeout}s)')
        raise
    except httpx.RequestError as e:
        logger.error(f'HTTP 请求异常: {method.upper()} {url}, 错误: {str(e)}')
        raise
