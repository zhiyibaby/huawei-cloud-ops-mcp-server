# 工具调用理解文档

本文档说明模型在调用工具时应遵循的规范和调用流程。所有工具均为异步函数，通过 MCP 协议调用。

## 工具概览

本 MCP 服务器提供以下工具（按优先级排序）：

| 工具名称 | 优先级 | 类别 | 说明 |
|---------|--------|------|------|
| `workflow_guide` | 0 | workflow | 工作流指导工具（最高优先级） |
| `prompt_understanding` | 1 | documentation | 理解 |
| `validate_account` | 2 | validation | 验证账号标识 |
| `get_huawei_api_docs` | 3 | documentation | 获取 API 文档 |
| `get_price_structure_doc` | 3 | price_documentation | 获取价格结构文档 |
| `query_price` | 5 | price_query | 查询价格信息 |
| `huawei_api_request` | 5 | api_request | 执行华为云 API 请求 |

## 工具详细说明

### 1. `workflow_guide` - 工作流指导工具

**优先级：0（最高）**  
**用途：** 根据用户查询自动分析需求类型，提供工具调用建议

**参数：**
- `query` (str, 必需): 用户的查询内容或需求描述

**返回值：** 字符串，包含工作流指导建议

**工作流规则：**
- 价格相关查询：先调用 `get_price_structure_doc`，再调用 `query_price`
- API 相关查询：先调用 `get_huawei_api_docs`，再调用 `huawei_api_request`
- 同时涉及价格和 API：优先处理价格查询

**使用建议：** 不确定如何开始时，先调用此工具获取指导。

### 2. `get_workflow_docs` - 获取工具调用文档

**优先级：1**  
**用途：** 返回完整的工具调用理解文档

**参数：** 无参数

**返回值：** 字符串，完整的工具调用文档内容（即本文档）

### 3. `validate_account` - 验证账号标识

**优先级：2**  
**用途：** 验证用户输入中是否包含有效的账号标识

**参数：**
- `query` (str, 必需): 用户的输入文本或查询内容

**返回值：** 字符串，账号验证结果信息
- 如果找到账号：返回确认信息（如 "检测到账号: xiaohei2018"）
- 如果未找到账号：返回提示信息，要求用户指定账号

**支持的账号：**
- `xiaohei2018`
- `krsk2021`

**使用建议：** 在执行需要账号的操作前，使用此工具验证用户是否已指定账号。

**示例：**
```python
# 包含账号的查询
validate_account("查询 xiaohei2018 的 ECS 实例")
# 返回: "✓ 检测到账号: xiaohei2018"

# 不包含账号的查询
validate_account("查询 ECS 实例列表")
# 返回: "✗ 未检测到账号标识\n请指定要使用的账号..."
```

### 4. `get_huawei_api_docs` - 获取 API 文档

**优先级：3**  
**用途：** 查询特定服务或所有服务的 API 文档说明

**参数：**
- `service` (str, 可选): 服务名称，默认 `None`
  - 可选值: `"ecs"`, `"vpc"`, `"rds"`, `"evs"`, `"elb"`, `"ims"`, `"ces"`
  - 如果未提供或为 `None`，返回所有服务的文档

**返回值：** 字符串，API 文档说明（Markdown 格式）

**示例：**
```python
# 获取所有服务的文档
get_huawei_api_docs()

# 获取 ECS 服务的文档
get_huawei_api_docs(service="ecs")
```

### 5. `get_price_structure_doc` - 获取价格结构文档

**优先级：3**  
**用途：** 获取指定服务的价格结构说明文档

**参数：**
- `service` (str, 可选): 服务名称，默认 `None`
  - 可选值: `"ecs"`, `"rds"`, `"evs"`, `"elb"` 等
  - 如果未提供，返回所有可用服务的列表

**返回值：** 字符串，价格结构文档（Markdown 格式）或可用服务列表

**示例：**
```python
# 获取所有可用服务列表
get_price_structure_doc()

# 获取 ECS 服务的价格结构文档
get_price_structure_doc(service="ecs")
```

### 6. `query_price` - 查询价格信息

**优先级：5**  
**用途：** 查询华为云服务的价格信息

**参数：**
- `service` (str, 必需): 服务名称，如 `"ecs"`, `"rds"`, `"evs"`, `"elb"`
- `filters` (Dict[str, str], 可选): 查询条件字典，支持模糊匹配
  - 支持的字段: `region`, `zone`, `cpu_arch`, `spec1`, `spec2`, `image`, `spec`
  - 示例: `{"region": "华北-北京四", "spec2": "Ac9s"}`
  - 注意: `spec` 字段会同时匹配 `spec1` 和 `spec2`
- `data_filters` (Dict[str, str], 可选): 价格表数据的过滤条件，支持模糊匹配
  - 支持按列名（表头）或列索引（从0开始）过滤
  - 示例: `{"规格名称": "large", "核数": "2核"}` 或 `{"0": "ac9s", "1": "2核"}`

**返回值：** 字符串，JSON 格式的查询结果，包含：
- `service`: 服务名称
- `filters`: 使用的查询条件
- `data_filters`: 使用的数据过滤条件
- `count`: 结果数量
- `results`: 价格数据列表

**特殊处理：**
- 如果查询区域为"北京一"，会自动映射到"北京四"

**示例：**
```python
# 查询所有 ECS 价格
query_price(service="ecs")

# 按区域查询
query_price(service="ecs", filters={"region": "华北-北京四"})

# 多条件查询
query_price(
    service="ecs",
    filters={"region": "华北-北京四", "spec2": "Ac9s"}
)

# 查询并过滤价格表数据
query_price(
    service="ecs",
    filters={"region": "华北-北京四"},
    data_filters={"规格名称": "large", "核数": "2核"}
)
```

### 7. `huawei_api_request` - 华为云 API 请求工具

**优先级：5**  
**用途：** 执行华为云 API 调用

**参数：**
- `service` (str, 必需): 服务类型
  - 支持: `"ecs"`, `"vpc"`, `"rds"`, `"evs"`, `"elb"`, `"ims"`, `"ces"`
- `action` (str, 必需): API 端点路径
  - 示例: `"v1/{project_id}/cloudservers/detail"`
  - 如果包含 `{project_id}`，工具会自动替换为对应区域的项目ID
- `method` (str, 可选): HTTP 方法，默认 `"GET"`
  - **注意：当前仅支持 GET 请求方式 和 LTS查询日志信息POST请求**
- `params` (Dict, 可选): 查询参数字典，用于 GET 请求的 URL 参数
  - 示例: `{"name": "test", "status": "ACTIVE", "limit": 50}`
  - 支持多个值: `{"tags": ["key1=value1", "key2=value2"]}`
- `data` (Dict, 可选): 请求体数据，用于 POST/PUT 请求
  - **注意：当前仅支持 GET 和 LTS查询日志信息POST请求，LTS查询时参数可用**
- `zone` (str, 可选): 区域名称，默认 `"华北-北京一"`
  - 工具会根据 `zone` 自动查找对应的 `project_id` 和 `region`
  - 支持的区域包括: `"华北-北京一"`, `"华北-北京四"`, `"华东-上海一"`, `"华东-上海二"`, `"华南-广州"` 等

**返回值：** 字符串，格式化的 JSON 字符串（包含缩进，中文不转义）

**自动处理：**
- `{project_id}` 占位符会自动替换为对应区域的项目ID
- 根据 `zone` 自动确定 `region` 和 `project_id`
- 自动使用环境变量中的认证信息

**示例：**
```python
# 查询所有 ECS 实例
huawei_api_request(
    service="ecs",
    action="v1/{project_id}/cloudservers/detail"
)

# 带查询参数
huawei_api_request(
    service="ecs",
    action="v1/{project_id}/cloudservers/detail",
    params={"name": "test", "status": "ACTIVE", "limit": 50}
)

# 指定区域
huawei_api_request(
    service="ecs",
    action="v1/{project_id}/cloudservers/detail",
    zone="华东-上海一"
)
```

## 调用流程

### 通用工作流程

1. **不确定如何开始时**：先调用 `workflow_guide(query="用户需求描述")` 获取工作流建议
2. **需要完整文档时**：调用 `get_workflow_docs()` 获取工具调用文档
3. **账号验证**：如果操作需要指定账号，先调用 `validate_account(query="用户输入")` 验证账号
4. **根据工作流建议**：按照建议的工具调用顺序执行操作

### API 查询操作流程

1. 如果不确定 API 端点，先调用 `get_huawei_api_docs(service="目标服务")` 获取文档
2. 根据文档确定正确的 `action` 和 `method`
3. 调用 `huawei_api_request(service="服务名称", action="API端点", method="GET", params={查询参数})` 执行操作
4. 解析返回的 JSON 结果

### 价格查询操作流程

1. 先调用 `get_price_structure_doc(service="服务名称")` 了解价格结构
2. 根据文档确定查询条件（`filters` 和 `data_filters`）
3. 调用 `query_price(service="服务名称", filters={查询条件}, data_filters={数据过滤条件})` 获取价格信息
4. 解析返回的 JSON 结果

## 关键注意事项

1. **工具优先级**：工具按优先级排序，`workflow_guide` 具有最高优先级（0），建议在不确定时先使用
2. **账号验证**：执行需要账号的操作前，使用 `validate_account` 验证用户是否指定了有效账号（支持：xiaohei2018、krsk2021）
3. **区域处理**：通过 `zone` 参数指定区域，工具会自动查找对应的 `project_id` 和 `region`，无需手动提供
4. **占位符替换**：`action` 中的 `{project_id}` 会自动替换，无需手动处理
5. **HTTP 方法限制**：`huawei_api_request` 当前仅支持 GET 请求方式，POST/PUT/DELETE 暂不支持
6. **参数格式**：严格按照工具定义传递参数，参数名称和类型必须匹配
7. **返回值格式**：所有工具返回字符串，JSON 格式的结果需要解析才能使用
8. **错误处理**：工具调用失败会抛出 `ValueError`，包含错误信息
9. **模糊匹配**：`query_price` 的 `filters` 和 `data_filters` 支持模糊匹配（子字符串匹配）
10. **区域映射**：查询"北京一"区域的价格时，会自动映射到"北京四"

## 常见服务端点参考

### ECS (弹性云服务器)
- 列表: `service="ecs"`, `action="v1/{project_id}/cloudservers/detail"`

### VPC (虚拟私有云)
- 列表: `service="vpc"`, `action="v1/{project_id}/vpcs"`
- 子网列表: `service="vpc"`, `action="v1/{project_id}/subnets"`

### RDS (关系型数据库)
- 列表: `service="rds"`, `action="v3/{project_id}/instances"`

### EVS (云硬盘)
- 列表: `service="evs"`, `action="v2/{project_id}/cloudvolumes"`

### ELB (弹性负载均衡)
- 列表: `service="elb"`, `action="v2/{project_id}/elb/loadbalancers"`

### IMS (镜像服务)
- 列表: `service="ims"`, `action="v2/images"`

### CES (云监控服务)
- 查询监控数据: `service="ces"`, `action="V1.0/{project_id}/metric-data"`, `params={"namespace": "...", "metric_name": "...", "from": "...", "to": "..."}`

## 最佳实践

1. **先获取指导**：不确定如何操作时，先调用 `workflow_guide` 获取建议
2. **账号验证优先**：在执行需要账号的操作前，先使用 `validate_account` 验证账号
3. **先查文档**：调用 API 或查询价格前，先获取相关文档了解结构
4. **逐步细化**：先进行简单查询，再根据结果添加过滤条件
5. **错误处理**：捕获 `ValueError` 异常，根据错误信息调整参数
6. **参数验证**：确保 `service` 参数是支持的服务之一
7. **区域选择**：明确指定 `zone` 参数，避免使用默认值导致的问题
