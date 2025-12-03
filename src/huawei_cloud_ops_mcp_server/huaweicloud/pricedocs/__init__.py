from importlib import resources
from functools import lru_cache


# 向后兼容：保留原有的字典（延迟加载，不立即填充）
PRICE_DBS = {}
PRICE_DOCS = {}

# 缓存文档路径，避免重复查找
_pricedocs_package = None
_price_doc_paths = {}


def _init_pricedocs():
    """初始化价格文档路径（延迟初始化）"""
    global _pricedocs_package, _price_doc_paths

    if _pricedocs_package is None:
        _pricedocs_package = resources.files(
            'huawei_cloud_ops_mcp_server.huaweicloud.pricedocs'
        )

        # 初始化 JSON 文件路径（价格数据库）
        json_files = [
            path
            for path in _pricedocs_package.iterdir()
            if path.is_file() and path.suffix == '.json'
        ]

        for json_path in json_files:
            # 例如: ecs_price.json -> ecs
            name = json_path.stem
            if name.endswith('_price'):
                service_name = name[:-6]  # 去掉 '_price' 后缀
                PRICE_DBS[service_name] = str(json_path)

        # 初始化价格文档路径（pricecomp 文件夹下的 md 文件）
        pricecomp_dir = _pricedocs_package / 'pricecomp'
        if pricecomp_dir.exists():
            md_files = [
                path
                for path in pricecomp_dir.iterdir()
                if path.is_file() and path.suffix == '.md'
            ]

            for md_path in md_files:
                service_name = md_path.stem.lower()
                _price_doc_paths[service_name] = md_path
                # 为了向后兼容，初始化空字符串（实际内容按需加载）
                PRICE_DOCS[service_name] = ''


@lru_cache(maxsize=None)
def get_price_doc(service_name: str) -> str:
    """
    获取价格文档内容（延迟加载 + 缓存）

    Args:
        service_name: 服务名称（小写），如 'ecs', 'rds'

    Returns:
        str: 价格文档内容

    Raises:
        RuntimeError: 如果文档文件不存在或读取失败
    """
    if _pricedocs_package is None:
        _init_pricedocs()

    service_name = service_name.lower()
    if service_name not in _price_doc_paths:
        raise ValueError(f'不支持的价格文档服务: {service_name}')

    md_path = _price_doc_paths[service_name]
    try:
        content = md_path.read_text(encoding='utf-8')
        # 更新 PRICE_DOCS 字典（向后兼容）
        PRICE_DOCS[service_name] = content
        return content
    except Exception as e:
        raise RuntimeError(f'无法读取价格文档文件 {md_path}: {e}')


def get_price_doc_names() -> list:
    """
    获取所有可用的价格文档服务名称列表

    Returns:
        list: 服务名称列表（小写）
    """
    if _pricedocs_package is None:
        _init_pricedocs()
    return list(_price_doc_paths.keys())
