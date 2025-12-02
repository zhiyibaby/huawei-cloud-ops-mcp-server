import asyncio
import importlib
import pkgutil
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server import tools
from huawei_cloud_ops_mcp_server.config import (
    MCP_TRANSPORT, MCP_HOST, MCP_PORT
)
from huawei_cloud_ops_mcp_server.logger import logger
from huawei_cloud_ops_mcp_server.common.register import (
    collect_tools_from_module
)
from huawei_cloud_ops_mcp_server.huaweicloud.static import (
    prompt_understanding_docs
)
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import (
    get_api_doc, get_api_doc_names
)
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
    get_price_doc, get_price_doc_names
)


def load_tools(mcp: FastMCP):
    """自动加载tools包下所有模块中的工具到MCP服务器,按优先级排序后注册"""
    tools_package = tools
    all_tools = []

    for finder, name, ispkg in pkgutil.iter_modules(
        tools_package.__path__, tools_package.__name__ + '.'
    ):
        # 跳过包和__init__.py
        if ispkg or name.endswith('.__init__'):
            continue
        try:
            module = importlib.import_module(name)
            module_tools = collect_tools_from_module(module)
            all_tools.extend(module_tools)
        except Exception as e:
            logger.warning(f'无法加载模块 {name}: {e}', exc_info=True)
            continue

    all_tools.sort(key=lambda x: x[0])

    # 按优先级顺序注册工具
    for priority, tool_func, tool_name in all_tools:
        try:
            mcp.tool(tool_func)
        except Exception as e:
            logger.warning(f'无法注册工具 {tool_name}: {e}', exc_info=True)
            continue

    logger.info(f'工具加载完成,共注册 {len(all_tools)} 个工具')


def load_resources(mcp: FastMCP):
    """
    加载资源到MCP服务器

    优化说明：
    1. 文档内容按需加载，不在启动时全部读取到内存
    2. 使用缓存机制，首次读取后缓存，避免重复读取文件
    3. 减少启动时的内存占用和 token 消耗
    """
    # prompt_understanding 资源（保持原有方式，因为文件较小且常用）
    @mcp.resource(uri='data://prompt_understanding')
    def prompt_understanding() -> str:
        """工具调用理解文档资源

        Returns:
            str: 工具调用理解文档内容
        """
        return prompt_understanding_docs

    # API 文档资源（延迟加载）
    api_doc_names = get_api_doc_names()
    for service_name in api_doc_names:
        # 使用闭包捕获 service_name，实现延迟加载
        def create_api_doc_handler(service: str):
            @mcp.resource(uri=f'data://api_docs/{service}')
            def api_doc() -> str:
                """华为云 API 文档资源（延迟加载）

                Returns:
                    str: API 文档内容
                """
                # 按需加载，首次加载后会缓存
                return get_api_doc(service)
            return api_doc

        create_api_doc_handler(service_name)

    # 价格文档资源（延迟加载）
    price_doc_names = get_price_doc_names()
    for service_name in price_doc_names:
        # 使用闭包捕获 service_name，实现延迟加载
        def create_price_doc_handler(service: str):
            @mcp.resource(uri=f'data://price_docs/{service}')
            def price_doc() -> str:
                """华为云价格数据结构文档资源（延迟加载）

                Returns:
                    str: 价格数据结构文档内容
                """
                # 按需加载，首次加载后会缓存
                return get_price_doc(service)
            return price_doc

        create_price_doc_handler(service_name)

    logger.info('资源加载完成')


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
    logger.info('=' * 60)
    logger.info('华为云运维 MCP 服务器启动')
    logger.info('=' * 60)
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT))
