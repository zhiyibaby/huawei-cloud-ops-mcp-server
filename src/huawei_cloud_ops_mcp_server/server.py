import inspect
import asyncio
import importlib
import pkgutil
from typing import List, Tuple, Callable
from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server import tools
from huawei_cloud_ops_mcp_server.config import MCP_TRANSPORT, MCP_HOST
from huawei_cloud_ops_mcp_server.logger import logger


def _collect_tools_from_class(tools_class) -> List[Tuple[int, Callable, str]]:
    """从类中收集工具及其优先级"""
    tools_list = []
    class_module = getattr(tools_class, '__module__', None)
    tool_metadatas = getattr(tools_class, 'tool_metadatas', {})
    for attr_name in dir(tools_class):
        # 跳过私有属性和元数据属性
        if attr_name.startswith('_') or attr_name.endswith('_metadata'):
            continue
        attr = getattr(tools_class, attr_name)
        attr_module = getattr(attr, '__module__', None)
        if attr_module and attr_module != class_module:
            continue
        # 收集静态方法
        if isinstance(
            inspect.getattr_static(tools_class, attr_name, None), staticmethod
        ):
            if callable(attr):
                metadata = tool_metadatas.get(attr_name)
                priority = metadata.priority if metadata else 10
                tools_list.append((priority, attr, attr_name))
        elif callable(attr) and not isinstance(attr, type):
            if inspect.isfunction(attr) or inspect.iscoroutinefunction(attr):
                # 获取优先级,如果不存在则使用默认值 10(最低优先级)
                metadata = tool_metadatas.get(attr_name)
                priority = metadata.priority if metadata else 10
                tools_list.append((priority, attr, attr_name))

    return tools_list


def _collect_tools_from_module(module) -> List[Tuple[int, Callable, str]]:
    """从模块中收集工具及其优先级"""
    tools_list = []
    module_name = module.__name__

    for attr_name in dir(module):
        if attr_name.startswith('_'):
            continue
        attr = getattr(module, attr_name)
        if inspect.isclass(attr):
            if getattr(attr, '__module__', None) == module_name:
                tools_list.extend(_collect_tools_from_class(attr))
        # 如果是函数或协程函数,直接收集
        elif (
            callable(attr) and
            (inspect.isfunction(attr) or inspect.iscoroutinefunction(attr))
        ):
            if getattr(attr, '__module__', None) == module_name:
                # 模块级函数默认优先级为 10(最低优先级)
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
            logger.debug(f'成功加载模块 {name},发现 {len(module_tools)} 个工具')
        except Exception as e:
            logger.warning(f'无法加载模块 {name}: {e}', exc_info=True)
            continue

    all_tools.sort(key=lambda x: x[0])

    # 按优先级顺序注册工具
    for priority, tool_func, tool_name in all_tools:
        try:
            mcp.tool(tool_func)
            logger.debug(f'成功注册工具 {tool_name} (优先级: {priority})')
        except Exception as e:
            logger.warning(f'无法注册工具 {tool_name}: {e}', exc_info=True)
            continue

    logger.info(f'工具加载完成,共注册 {len(all_tools)} 个工具')


def main(mcp: FastMCP, transport: str):
    logger.info(f'启动 MCP 服务器,传输方式: {transport}')
    load_tools(mcp)
    mcp.run(transport=transport)


async def main_async(mcp: FastMCP, transport: str, host: str = None):
    logger.info(f'启动 MCP 服务器(异步模式),传输方式: {transport}')
    if transport == 'http':
        logger.info(f'HTTP 模式,监听地址: {host}')
    load_tools(mcp)
    if transport == 'http':
        await mcp.run_async(transport=transport, host=host)
    else:
        await mcp.run_async(transport=transport)


if __name__ == '__main__':
    logger.info('=' * 60)
    logger.info('华为云运维 MCP 服务器启动')
    logger.info('=' * 60)
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST))
