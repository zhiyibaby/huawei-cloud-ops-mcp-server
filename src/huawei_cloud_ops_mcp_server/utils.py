import json
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ToolMetadata:
    priority: int  # 1-10, 1为最高优先级
    category: str  # 工具分类
    timeout: int   # 超时时间
    retryable: bool  # 是否可重试


def strict_error_handler(func):
    """
    用于函数的严格错误处理装饰器.
    所有异常都会被捕获，返回统一结构体，不进行重试、降级，便于前端或调用方识别和处理.

    返回内容结构:
    {
        "content": [{"type": "text", "text": str}],
        "isError": True
    }
    """

    import functools
    import traceback
    import inspect

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # 检查函数是否是协程函数
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                # 同步函数直接调用
                return func(*args, **kwargs)
        except Exception as e:
            # 直接返回详细错误信息(含traceback)，不进行任何重试或降级
            err_text = f'工具执行失败: {str(e)}'
            tb = traceback.format_exc()
            return {
                'content': [
                    {
                        'type': 'text',
                        'text': err_text
                    },
                    {
                        'type': 'error_detail',
                        'text': tb
                    }
                ],
                'isError': True,
                'errorType': str(e.__class__.__name__),
            }
    return wrapper


def http_request(
    method: str,
    url: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    json_data: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    通用的 HTTP 请求函数

    Args:
        method: HTTP 方法 (GET, POST, PUT, DELETE, PATCH 等)
        url: 请求的 URL
        data: 请求体数据（字典格式，会被序列化为 JSON）
        params: URL 查询参数字典
        headers: 自定义请求头字典（可选）
        timeout: 请求超时时间（秒），默认 30
        json_data: 直接传递的 JSON 数据
            （如果提供，将优先使用此参数而不是 data）

    Returns:
        Dict[str, Any]: 包含 status_code 和 data 的字典
        {
            'status_code': int,
            'data': dict 或 {'text': str}
        }

    示例:
        # GET 请求
        response = http_request(
            'GET', 'https://api.example.com/users', params={'page': 1}
        )

        # POST 请求
        response = http_request(
            'POST', 'https://api.example.com/users',
            data={'name': 'John', 'age': 30}
        )

        # 带自定义请求头
        response = http_request(
            'GET', 'https://api.example.com/data',
            headers={'Authorization': 'Bearer token'}
        )
    """
    # 设置默认请求头
    request_headers = {
        'Content-Type': 'application/json',
    }
    if headers:
        request_headers.update(headers)

    # 处理请求体
    body = None
    if json_data is not None:
        body = json.dumps(json_data)
    elif data is not None:
        body = json.dumps(data)

    # 发送请求
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=request_headers,
        params=params,
        data=body,
        timeout=timeout
    )

    # 解析响应
    try:
        result = response.json()
    except json.JSONDecodeError:
        result = {'text': response.text}

    return {
        'status_code': response.status_code,
        'data': result
    }
