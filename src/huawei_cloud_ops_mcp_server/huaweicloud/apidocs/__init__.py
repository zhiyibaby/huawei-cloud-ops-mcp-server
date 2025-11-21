from importlib import resources

from huawei_cloud_ops_mcp_server.logger import logger

API_DOCS = {}
SUPPORTED_SERVICES = []

apidocs_package = resources.files(
    'huawei_cloud_ops_mcp_server.huaweicloud.apidocs'
)
services = [
    path.stem
    for path in apidocs_package.iterdir()
    if path.is_file() and path.suffix == '.md'
]

for name in services:
    md_path = apidocs_package.joinpath(f'{name}.md')
    try:
        API_DOCS[name.lower()] = md_path.read_text(encoding='utf-8')
        SUPPORTED_SERVICES.append(name.lower())
    except Exception as e:
        logger.warning(f'无法读取API文档文件 {md_path}: {e}')
