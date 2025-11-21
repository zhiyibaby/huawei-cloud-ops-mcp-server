from importlib import resources

PRICE_DOCS = {}

pricedocs_package = resources.files(
    'huawei_cloud_ops_mcp_server.huaweicloud.pricedocs'
)

json_files = [
    path
    for path in pricedocs_package.iterdir()
    if path.is_file() and path.suffix == '.json'
]

# 构建字典，从文件名中提取服务名称（去掉 _price.json 后缀）
for json_path in json_files:
    # 例如: ecs_price.json -> ecs
    name = json_path.stem
    if name.endswith('_price'):
        service_name = name[:-6]  # 去掉 '_price' 后缀
        PRICE_DOCS[service_name] = str(json_path)
