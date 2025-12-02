from importlib import resources
from functools import lru_cache


# 向后兼容：保留原有的字典（延迟加载，不立即填充）
API_DOCS = {}
SUPPORTED_SERVICES = []

# 缓存文档路径，避免重复查找
_apidocs_package = None
_api_doc_paths = {}


def _init_apidocs():
    """初始化 API 文档路径（延迟初始化）"""
    global _apidocs_package, _api_doc_paths
    if _apidocs_package is None:
        _apidocs_package = resources.files(
            'huawei_cloud_ops_mcp_server.huaweicloud.apidocs'
        )
        services = [
            path.stem
            for path in _apidocs_package.iterdir()
            if path.is_file() and path.suffix == '.md'
        ]
        for name in services:
            service_name = name.lower()
            md_path = _apidocs_package.joinpath(f'{name}.md')
            _api_doc_paths[service_name] = md_path
            SUPPORTED_SERVICES.append(service_name)
            API_DOCS[service_name] = ''


@lru_cache(maxsize=None)
def get_api_doc(service_name: str) -> str:
    """
    获取 API 文档内容（延迟加载 + 缓存）

    Args:
        service_name: 服务名称（小写），如 'ecs', 'vpc'

    Returns:
        str: API 文档内容

    Raises:
        RuntimeError: 如果文档文件不存在或读取失败
    """
    if _apidocs_package is None:
        _init_apidocs()

    service_name = service_name.lower()
    if service_name not in _api_doc_paths:
        raise ValueError(f'不支持的 API 文档服务: {service_name}')

    md_path = _api_doc_paths[service_name]
    try:
        content = md_path.read_text(encoding='utf-8')
        # 更新 API_DOCS 字典（向后兼容）
        API_DOCS[service_name] = content
        return content
    except Exception as e:
        raise RuntimeError(f'无法读取API文档文件 {md_path}: {e}')


def get_api_doc_names() -> list:
    """
    获取所有可用的 API 文档服务名称列表

    Returns:
        list: 服务名称列表（小写）
    """
    if _apidocs_package is None:
        _init_apidocs()
    return list(_api_doc_paths.keys())


# 延迟初始化：不在模块导入时初始化，而是在第一次使用时初始化
# _init_apidocs()  # 注释掉，改为在 get_api_doc_names() 中调用
