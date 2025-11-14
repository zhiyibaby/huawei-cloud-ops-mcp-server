from importlib import resources

with (
    resources.files('huawei_cloud_ops_mcp_server.huaweicloud.static')
    .joinpath('PROMPT_UNDERSTANDING.md')
    .open('r', encoding='utf-8') as f
):
    prompt_understanding_docs = f.read()

with (
    resources.files('huawei_cloud_ops_mcp_server.huaweicloud.static')
    .joinpath('API_OPERATIONS.md')
    .open('r', encoding='utf-8') as f
):
    api_operations_docs = f.read()
