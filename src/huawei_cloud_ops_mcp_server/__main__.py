import asyncio
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.server import main_async


if __name__ == "__main__":
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    # main(mcp, 'http')
    asyncio.run(main_async(mcp, 'http'))
