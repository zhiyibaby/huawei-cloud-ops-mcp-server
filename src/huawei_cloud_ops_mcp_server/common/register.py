import inspect
import importlib
import pkgutil
from typing import List, Tuple, Callable

from fastmcp import FastMCP

from huawei_cloud_ops_mcp_server.config.logger import logger
from huawei_cloud_ops_mcp_server import tools
from huawei_cloud_ops_mcp_server.huaweicloud.static import (
    prompt_understanding_docs
)
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import (
    get_api_doc, get_api_doc_names
)
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
    get_price_doc, get_price_doc_names
)


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
    """ 加载资源到MCP服务器"""

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
