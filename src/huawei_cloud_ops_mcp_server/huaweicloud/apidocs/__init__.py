from importlib import resources

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
    md_path = (apidocs_package.joinpath(f'{name}.md'))
    with md_path.open('r', encoding='utf-8') as f:
        API_DOCS[name.lower()] = f.read()
        SUPPORTED_SERVICES.append(name.lower())
