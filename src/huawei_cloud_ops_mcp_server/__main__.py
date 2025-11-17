import asyncio
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.server import main_async
from huawei_cloud_ops_mcp_server.config import MCP_TRANSPORT, MCP_HOST


if __name__ == "__main__":
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )

    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST))
