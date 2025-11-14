import asyncio
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.server import main_async
from huawei_cloud_ops_mcp_server.config import MCP_TRANSPORT


if __name__ == "__main__":
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    # 从环境变量或 .env 文件读取传输方式，默认为 stdio
    asyncio.run(main_async(mcp, MCP_TRANSPORT))
