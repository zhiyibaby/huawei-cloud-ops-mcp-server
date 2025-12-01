import inspect
import asyncio
import importlib
import pkgutil
from typing import List, Tuple, Callable
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server import tools
from huawei_cloud_ops_mcp_server.config import (
    MCP_TRANSPORT, MCP_HOST, MCP_PORT
)
from huawei_cloud_ops_mcp_server.logger import logger
from huawei_cloud_ops_mcp_server.huaweicloud.static import (
    prompt_understanding_docs
)
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import API_DOCS
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import PRICE_DOCS


def _collect_tools_from_class(cls) -> List[Tuple[int, Callable, str]]:
    """
    从类中收集工具及其优先级
    返回: List[Tuple[priority, func, name]]
    """
    tools_list = []
    class_module = getattr(cls, '__module__', None)
    tool_metadatas = getattr(cls, 'tool_metadatas', {})
    for attr_name in dir(cls):
        if attr_name.startswith('_') or attr_name.endswith('_metadata'):
            continue
        attr = getattr(cls, attr_name)
        # 只收集当前类本模块的方法
        if getattr(attr, '__module__', None) != class_module:
            continue
        # 静态方法、类方法、普通方法
        staticattr = inspect.getattr_static(cls, attr_name, None)
        if isinstance(staticattr, (staticmethod, classmethod)):
            func = attr
        elif callable(attr) and not isinstance(attr, type):
            func = attr
        else:
            continue
        if callable(func):
            metadata = tool_metadatas.get(attr_name)
            priority = getattr(metadata, 'priority', 10) if metadata else 10
            tools_list.append((priority, func, attr_name))
    return tools_list


def _collect_tools_from_module(module) -> List[Tuple[int, Callable, str]]:
    """从模块中收集工具及其优先级"""
    tools_list = []
    module_name = module.__name__
    for attr_name in dir(module):
        if attr_name.startswith('_'):
            continue
        attr = getattr(module, attr_name)
        if (
            inspect.isclass(attr)
            and getattr(attr, '__module__', None) == module_name
        ):
            tools_list.extend(_collect_tools_from_class(attr))
        elif (
            callable(attr)
            and (inspect.isfunction(attr) or inspect.iscoroutinefunction(attr))
            and getattr(attr, '__module__', None) == module_name
        ):
            tools_list.append((10, attr, attr_name))
    return tools_list


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
            module_tools = _collect_tools_from_module(module)
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
    """加载资源到MCP服务器"""

    # 注册 prompt_understanding 资源
    @mcp.resource(uri="data://prompt_understanding")
    def prompt_understanding() -> str:
        """工具调用理解文档资源

        Returns:
            str: 工具调用理解文档内容
        """
        return prompt_understanding_docs

    # 注册所有服务的 API 文档资源
    for service_name, doc_content in API_DOCS.items():
        uri = f"data://api_docs/{service_name}"

        def create_api_doc_handler(res_uri: str, content: str):
            @mcp.resource(uri=res_uri)
            def api_doc() -> str:
                """华为云 API 文档资源

                Returns:
                    str: API 文档内容
                """
                return content
            return api_doc

        create_api_doc_handler(uri, doc_content)

    # 注册所有服务的价格文档资源
    for service_name, doc_content in PRICE_DOCS.items():
        uri = f"data://price_docs/{service_name}"

        def create_price_doc_handler(res_uri: str, content: str):
            @mcp.resource(uri=res_uri)
            def price_doc() -> str:
                """华为云价格数据结构文档资源

                Returns:
                    str: 价格数据结构文档内容
                """
                return content
            return price_doc

        create_price_doc_handler(uri, doc_content)

    logger.info(
        f'资源加载完成: '
        f'已注册 prompt_understanding 资源、'
        f'{len(API_DOCS)} 个 API 文档资源和 '
        f'{len(PRICE_DOCS)} 个价格文档资源'
    )


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
