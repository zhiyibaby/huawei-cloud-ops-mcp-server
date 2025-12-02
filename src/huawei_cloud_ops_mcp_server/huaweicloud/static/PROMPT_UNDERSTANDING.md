# 工具调用理解文档

本文档说明模型在调用工具时应遵循的规范和调用流程。所有工具均为异步函数，通过 MCP 协议调用。

## 工具概览

本 MCP 服务器提供以下工具（按优先级排序）：

| 工具名称 | 优先级 | 类别 | 说明 |
|---------|--------|------|------|
| `workflow_guide` | 0 | workflow | 工作流指导工具（最高优先级） |
| `elicit_service_info` | 2 | elicit | 引导用户补全服务信息 |
| `validate_account` | 1 | validation | 验证账号标识 |
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
- 价格相关查询：先通过 Resource URI `data://price_docs/{service}` 获取价格文档，再调用 `query_price`
- API 相关查询：先通过 Resource URI `data://api_docs/{service}` 获取 API 文档，再调用 `huawei_api_request`
- 同时涉及价格和 API：优先处理价格查询

**使用建议：** 不确定如何开始时，先调用此工具获取指导。

### 2. `elicit_service_info` - 引导用户补全服务信息

**优先级：2**  
**用途：** 当用户输入不明确（没有明确指定服务类型）时，引导用户补全服务信息

**参数：**
- `query` (str, 必需): 用户的输入文本或查询内容

**返回值：** 字符串，JSON 格式的补全结果，包含：
- `service`: 服务代码（如 "ecs", "vpc"）
- `query_type`: 查询类型（"price" 或 "api"）
- `original_query`: 原始查询文本
- `message`: 补全过程的详细信息

**特殊功能：**
- 自动判断查询类型（价格查询或 API 查询）
- 如果无法从输入中提取服务名称，会通过 `elicit` 询问用户选择服务
- 根据查询类型显示相应的可用服务列表

**使用建议：** 当用户查询不明确（如"查询价格"、"查询实例"）时，使用此工具引导用户补全服务类型。

### 3. `validate_account` - 验证账号标识

**优先级：1**  
**用途：** 验证用户输入中是否包含有效的账号标识，或通过 Authorization 请求头认证

**参数：**
- `query` (str, 必需): 用户的输入文本或查询内容

**返回值：** 字符串，账号验证结果信息
- 如果请求头包含 Authorization：返回确认信息
- 如果找到账号：返回确认信息（如 "检测到账号: xiaohei2018"）
- 如果未找到账号：通过 `elicit` 询问用户选择账号

**支持的账号：** xiaohei2018, krsk2021

**特殊功能：**
- 优先检查请求头中的 Authorization 认证信息
- 如果无 Authorization 且输入中无账号，会通过 `elicit` 询问用户选择账号
- 验证用户选择的账号是否在支持列表中

**使用建议：** 在执行需要账号的 API 操作前，使用此工具验证用户是否已指定账号。

### 4. `query_price` - 查询价格信息

**优先级：5**  
**用途：** 查询华为云服务的价格信息

**参数：**
- `service` (str, 可选): 服务名称，默认 `"ecs"`，支持 `"ecs"`, `"rds"`, `"evs"`, `"elb"` 等
- `filters` (Dict[str, str], 可选): 查询条件字典，支持模糊匹配
  - 支持的字段: `region`, `zone`, `cpu_arch`, `spec1`, `spec2`, `image`, `spec`
  - 示例: `{"region": "华北-北京四", "spec2": "Ac9s"}`
  - 注意: `spec` 字段会同时匹配 `spec1` 和 `spec2`
- `data_filters` (Dict[str, str], 可选): 价格表数据的过滤条件，支持模糊匹配
  - 支持按列名（表头）或列索引（从0开始）过滤
  - 示例: `{"规格名称": "large", "核数": "2核"}` 或 `{"0": "ac9s", "1": "2核"}`
- `page` (int, 可选): 页码，从1开始，默认值为 `1`
- `page_size` (int, 可选): 每页记录数，默认值为 `50`

**返回值：** 字符串，JSON 格式的查询结果（中文不转义），包含：
- `service`: 服务名称
- `filters`: 使用的查询条件
- `data_filters`: 使用的数据过滤条件
- `pagination`: 分页信息对象
  - `page`: 当前页码
  - `page_size`: 每页记录数
  - `total_count`: 总记录数
  - `total_pages`: 总页数
  - `has_next`: 是否有下一页
  - `has_prev`: 是否有上一页
- `count`: 当前页的结果数量
- `results`: 当前页的价格数据列表

**特殊处理：**
- 如果查询区域为"北京一"，会自动映射到"北京四"
- 分页查询：当结果数量较多时，使用 `page` 和 `page_size` 参数进行分页查询，每页默认返回50条记录

### 5. `huawei_api_request` - 华为云 API 请求工具

**优先级：5**  
**用途：** 执行华为云 API 调用

**参数：**
- `account` (str, 必需): 账号名称，如 `"xiaohei2018"`, `"krsk2021"`
- `service` (str, 必需): 服务类型
  - 支持: `"ecs"`, `"vpc"`, `"rds"`, `"evs"`, `"elb"`, `"ims"`, `"ces"`, `"lts"`, `"obs"`, `"eip"`, `"dds"`, `"css"`, `"dcs"`
- `action` (str, 必需): API 端点路径
  - 示例: `"v1/{project_id}/cloudservers/detail"`
  - 如果包含 `{project_id}`，工具会自动替换为对应区域的项目ID
- `method` (str, 可选): HTTP 方法，默认 `"GET"`
  - **注意：当前仅支持 GET 请求方式和 LTS 查询日志信息 POST 请求**
- `params` (Dict, 可选): 查询参数字典，用于 GET 请求的 URL 参数
  - 示例: `{"name": "test", "status": "ACTIVE", "limit": 50}`
  - 支持多个值: `{"tags": ["key1=value1", "key2=value2"]}`
- `data` (Dict, 可选): 请求体数据，用于 POST/PUT 请求
  - **注意：当前仅支持 LTS 查询日志信息 POST 请求时可用**
- `zone` (str, 可选): 区域名称，默认 `"华北-北京一"`
  - 工具会根据 `zone` 自动查找对应的 `project_id` 和 `region`
  - 支持的区域包括: `"华北-北京一"`, `"华北-北京四"`, `"华东-上海一"`, `"华东-上海二"`, `"华南-广州"` 等

**返回值：** 字符串，JSON 格式的 API 响应结果（中文不转义）

**自动处理：**
- `{project_id}` 占位符会自动替换为对应区域的项目ID
- 根据 `zone` 自动确定 `region` 和 `project_id`
- 根据 `account` 参数使用对应账号的认证信息

## 资源说明

### `prompt_understanding` - 工具调用理解文档资源

**资源 URI：** `data://prompt_understanding`  
**用途：** 提供完整的工具调用规范和工作流程说明文档（即本文档）

**访问方式：** 通过 MCP 资源协议访问，无需调用工具函数。客户端可以通过资源 URI `data://prompt_understanding` 获取本文档的完整内容。

### `api_docs/{service}` - API 文档资源

**资源 URI：** `data://api_docs/{service}`  
**用途：** 提供指定服务的 API 文档说明

**参数：**
- `{service}`: 服务名称，如 `"ecs"`, `"vpc"`, `"rds"`, `"evs"`, `"elb"`, `"ims"`, `"ces"` 等

**访问方式：** 通过 MCP 资源协议访问，无需调用工具函数。客户端可以通过资源 URI `data://api_docs/{service}` 获取指定服务的 API 文档。

**示例：**
- `data://api_docs/ecs` - 获取 ECS 服务的 API 文档
- `data://api_docs/vpc` - 获取 VPC 服务的 API 文档

### `price_docs/{service}` - 价格数据结构文档资源

**资源 URI：** `data://price_docs/{service}`  
**用途：** 提供指定服务的价格结构说明文档

**参数：**
- `{service}`: 服务名称，如 `"ecs"`, `"rds"`, `"evs"`, `"elb"` 等

**访问方式：** 通过 MCP 资源协议访问，无需调用工具函数。客户端可以通过资源 URI `data://price_docs/{service}` 获取指定服务的价格结构文档。

**示例：**
- `data://price_docs/ecs` - 获取 ECS 服务的价格结构文档
- `data://price_docs/rds` - 获取 RDS 服务的价格结构文档

## 调用流程

### 通用工作流程

1. **不确定如何开始时**：先调用 `workflow_guide(query="用户需求描述")` 获取工作流建议
2. **需要完整文档时**：通过 Resource URI `data://prompt_understanding` 获取工具调用文档
3. **服务信息不明确时**：调用 `elicit_service_info(query="用户输入")` 引导用户补全服务信息
4. **账号验证**：如果操作需要指定账号，先调用 `validate_account(query="用户输入")` 验证账号
5. **根据工作流建议**：按照建议的工具调用顺序执行操作

### API 查询操作流程

1. 如果用户查询不明确，先调用 `elicit_service_info(query="用户输入")` 确定服务类型
2. 调用 `validate_account(query="用户输入")` 验证账号信息
3. 如果不确定 API 端点，先通过 Resource URI `data://api_docs/{service}` 获取 API 文档
4. 根据文档确定正确的 `action` 和 `method`
5. 调用 `huawei_api_request(account="账号名称", service="服务名称", action="API端点", method="GET", params={查询参数})` 执行操作
6. 解析返回的 JSON 结果

### 价格查询操作流程

1. 如果用户查询不明确，先调用 `elicit_service_info(query="用户输入")` 确定服务类型
2. 通过 Resource URI `data://price_docs/{service}` 获取价格结构文档，了解价格结构
3. 根据文档确定查询条件（`filters` 和 `data_filters`）
4. 调用 `query_price(service="服务名称", filters={查询条件}, data_filters={数据过滤条件}, page=1, page_size=50)` 获取价格信息
5. 如果结果数量较多，可以通过 `page` 和 `page_size` 参数进行分页查询
6. 解析返回的 JSON 结果，使用 `pagination` 信息判断是否有更多页数据

## 关键注意事项

1. **工具优先级**：工具按优先级排序，`workflow_guide` 具有最高优先级（0），`elicit_service_info` 优先级为1，建议在不确定时先使用
2. **服务信息补全**：当用户查询不明确时，使用 `elicit_service_info` 引导用户补全服务信息，工具会通过交互式询问确定服务类型
3. **账号验证**：执行需要账号的 API 操作前，使用 `validate_account` 验证用户是否指定了有效账号（支持：xiaohei2018、krsk2021）
4. **交互式确认**：`validate_account` 和 `elicit_service_info` 会在必要时通过 `elicit` 询问用户，确保获得正确的参数
5. **账号参数必需**：`huawei_api_request` 需要明确指定 `account` 参数，可通过 `validate_account` 获取
6. **区域处理**：通过 `zone` 参数指定区域，工具会自动查找对应的 `project_id` 和 `region`，无需手动提供
7. **占位符替换**：`action` 中的 `{project_id}` 会自动替换，无需手动处理
8. **HTTP 方法限制**：`huawei_api_request` 当前仅支持 GET 请求方式和 LTS 日志查询 POST 请求，其他 POST/PUT/DELETE 请求暂不支持
9. **参数格式**：严格按照工具定义传递参数，参数名称和类型必须匹配
10. **返回值格式**：所有工具返回字符串，JSON 格式的结果需要解析才能使用（中文不转义）
11. **错误处理**：工具调用失败会抛出 `ValueError`，包含错误信息
12. **模糊匹配**：`query_price` 的 `filters` 和 `data_filters` 支持模糊匹配（子字符串匹配）
13. **区域映射**：查询"北京一"区域的价格时，会自动映射到"北京四"
14. **分页查询**：`query_price` 支持分页查询，默认每页50条记录，可通过 `page` 和 `page_size` 参数控制分页

## 最佳实践

1. **先获取指导**：不确定如何操作时，先调用 `workflow_guide` 获取建议
2. **服务信息补全**：用户查询不明确时，使用 `elicit_service_info` 引导用户补全服务类型
3. **账号验证优先**：在执行需要账号的 API 操作前，先使用 `validate_account` 验证账号
4. **信任交互式工具**：`validate_account` 和 `elicit_service_info` 会在需要时主动询问用户，确保获得正确信息
5. **先查文档**：调用 API 或查询价格前，先获取相关文档了解结构
6. **逐步细化**：先进行简单查询，再根据结果添加过滤条件
7. **错误处理**：捕获 `ValueError` 异常，根据错误信息调整参数
8. **参数验证**：确保 `service` 参数是支持的服务之一
9. **区域选择**：明确指定 `zone` 参数，避免使用默认值导致的问题
10. **账号参数传递**：调用 `huawei_api_request` 时务必传递 `account` 参数
