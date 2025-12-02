import asyncio
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.server import main_async
from huawei_cloud_ops_mcp_server.config import (
    MCP_TRANSPORT, MCP_HOST, MCP_PORT
)
from huawei_cloud_ops_mcp_server.config.logger import logger


if __name__ == "__main__":
    logger.info('=' * 60)
    logger.info('华为云运维 MCP 服务器启动')
    logger.info('=' * 60)
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )

    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT))
