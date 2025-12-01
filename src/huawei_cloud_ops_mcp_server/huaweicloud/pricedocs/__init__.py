from importlib import resources


PRICE_DBS = {}
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
        PRICE_DBS[service_name] = str(json_path)

# 导入 pricecomp 文件夹下的 md 文件
pricecomp_dir = pricedocs_package / 'pricecomp'
md_files = [
    path
    for path in pricecomp_dir.iterdir()
    if path.is_file() and path.suffix == '.md'
]

for md_path in md_files:
    service_name = md_path.stem.lower()
    try:
        PRICE_DOCS[service_name] = md_path.read_text(encoding='utf-8')
    except Exception as e:
        raise RuntimeError(f'无法读取价格文档文件 {md_path}: {e}')
