import inspect
from typing import List, Tuple, Callable


def collect_tools_from_class(cls) -> List[Tuple[int, Callable, str]]:
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


def collect_tools_from_module(module) -> List[Tuple[int, Callable, str]]:
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
            tools_list.extend(collect_tools_from_class(attr))
        elif (
            callable(attr)
            and (inspect.isfunction(attr) or inspect.iscoroutinefunction(attr))
            and getattr(attr, '__module__', None) == module_name
        ):
            tools_list.append((10, attr, attr_name))
    return tools_list
