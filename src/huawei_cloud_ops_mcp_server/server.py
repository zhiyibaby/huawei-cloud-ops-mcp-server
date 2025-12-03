import asyncio
import functools
from typing import Any, Callable

from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.config import (
    MCP_TRANSPORT, MCP_HOST, MCP_PORT
)
from huawei_cloud_ops_mcp_server.common.register import (
    load_tools, load_resources
)
from huawei_cloud_ops_mcp_server.config.logger import logger
from huawei_cloud_ops_mcp_server.config import (
    TOOLS_REQUIRE_ACCOUNT, TOOLS_REQUIRE_SERVICE
)
from huawei_cloud_ops_mcp_server.common.flow import validate_tool_params


def tool_execution_hook(original_func: Callable) -> Callable:
    """工具执行钩子装饰器

    在工具执行前进行参数验证（账号、服务等）

    Args:
        original_func: 原始工具函数

    Returns:
        Callable: 包装后的工具函数
    """
    @functools.wraps(original_func)
    async def wrapper(*args, **kwargs) -> Any:
        tool_name = original_func.__name__

        if tool_name in (TOOLS_REQUIRE_ACCOUNT | TOOLS_REQUIRE_SERVICE):
            ctx = kwargs.get('ctx')
            tool_kwargs = {k: v for k, v in kwargs.items() if k != 'ctx'}
            await validate_tool_params(tool_name, tool_kwargs, ctx)
            for key, value in tool_kwargs.items():
                if key != 'ctx':
                    kwargs[key] = value
        return await original_func(*args, **kwargs)

    return wrapper


def main(mcp: FastMCP, transport: str):
    logger.info(f'启动 MCP 服务器,传输方式: {transport}')
    load_tools(mcp)
    load_resources(mcp)
    mcp.run(transport=transport)


async def main_async(
    mcp: FastMCP, transport: str, host: str = None, port: int = None
):
    logger.info(f'启动 MCP 服务器(异步模式),传输方式: {transport}')
    if transport == 'http':
        logger.info(f'HTTP 模式,监听地址: {host}:{port}')
    load_tools(mcp)
    load_resources(mcp)
    if transport == 'http':
        await mcp.run_async(transport=transport, host=host, port=port)
    else:
        await mcp.run_async(transport=transport)


if __name__ == '__main__':
    logger.info('华为云运维 MCP 服务器启动')
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT))
