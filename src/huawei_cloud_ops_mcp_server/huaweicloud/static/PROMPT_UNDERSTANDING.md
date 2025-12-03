# 工具调用理解文档

本文档说明模型在调用工具时应遵循的规范和调用流程。所有工具均为异步函数，通过 MCP 协议调用。

## 工具概览

本 MCP 服务器提供以下工具（按优先级排序）：

| 工具名称 | 优先级 | 类别 | 说明 |
|---------|--------|------|------|
| `workflow_guide` | 0 | workflow | 工作流指导工具（最高优先级） |
| `query_price` | 5 | price_query | 查询价格信息（含自动验证钩子） |
| `huawei_api_request` | 5 | api_request | 执行华为云 API 请求（含自动验证钩子） |

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

### 2. `query_price` - 查询价格信息（含自动验证）

**优先级：5**  
**用途：** 查询华为云服务的价格信息

**🔒 自动验证：** 工具执行前会自动验证服务参数，如果缺少会抛出友好的错误提示

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

### 3. `huawei_api_request` - 华为云 API 请求工具（含自动验证）

**优先级：5**  
**用途：** 执行华为云 API 调用

**🔒 自动验证：** 工具执行前会自动验证账号和服务参数，如果缺少会抛出友好的错误提示

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

### 通用工作流程（简化版）

由于工具执行钩子已启用，调用流程更加简化：

1. **不确定如何开始时**：先调用 `workflow_guide(query="用户需求描述")` 获取工作流建议
2. **需要完整文档时**：通过 Resource URI `data://prompt_understanding` 获取工具调用文档
3. **直接调用目标工具**：钩子会自动验证账号和服务参数，如果缺少会自动提示

### API 查询操作流程（简化版）

1. 如果不确定 API 端点，先通过 Resource URI `data://api_docs/{service}` 获取 API 文档
2. 根据文档确定正确的 `action` 和 `method`
3. **直接调用** `huawei_api_request(account="账号名称", service="服务名称", action="API端点", method="GET", params={查询参数})`
   - 钩子会自动验证账号（支持：xiaohei2018、krsk2021）
   - 钩子会自动验证服务参数
   - 如果缺少参数，会抛出友好的错误提示
4. 解析返回的 JSON 结果

### 价格查询操作流程（简化版）

1. 通过 Resource URI `data://price_docs/{service}` 获取价格结构文档，了解价格结构
2. 根据文档确定查询条件（`filters` 和 `data_filters`）
3. **直接调用** `query_price(service="服务名称", filters={查询条件}, data_filters={数据过滤条件}, page=1, page_size=50)`
   - 钩子会自动验证服务参数
   - 如果缺少参数，会抛出友好的错误提示
4. 如果结果数量较多，可以通过 `page` 和 `page_size` 参数进行分页查询
5. 解析返回的 JSON 结果，使用 `pagination` 信息判断是否有更多页数据

## 关键注意事项

1. **🔒 工具执行钩子**：`huawei_api_request` 和 `query_price` 已启用自动验证钩子
   - 账号验证：自动检查账号参数（支持：xiaohei2018、krsk2021）或 Authorization 请求头
   - 服务验证：自动检查服务参数，支持多种服务（ecs, vpc, rds, evs, elb 等）
   - 缺少参数时会抛出友好的错误提示，列出可用选项
2. **工具优先级**：工具按优先级排序，`workflow_guide` 具有最高优先级（0），建议在不确定时先使用
3. **账号参数必需**：`huawei_api_request` 需要明确指定 `account` 参数，钩子会验证其有效性
4. **区域处理**：通过 `zone` 参数指定区域，工具会自动查找对应的 `project_id` 和 `region`，无需手动提供
5. **占位符替换**：`action` 中的 `{project_id}` 会自动替换，无需手动处理
6. **HTTP 方法限制**：`huawei_api_request` 当前仅支持 GET 请求方式和 LTS 日志查询 POST 请求，其他 POST/PUT/DELETE 请求暂不支持
7. **参数格式**：严格按照工具定义传递参数，参数名称和类型必须匹配
8. **返回值格式**：所有工具返回字符串，JSON 格式的结果需要解析才能使用（中文不转义）
9. **错误处理**：工具调用失败会抛出异常，包含详细的错误信息和可用选项
10. **模糊匹配**：`query_price` 的 `filters` 和 `data_filters` 支持模糊匹配（子字符串匹配）
11. **区域映射**：查询"北京一"区域的价格时，会自动映射到"北京四"
12. **分页查询**：`query_price` 支持分页查询，默认每页50条记录，可通过 `page` 和 `page_size` 参数控制分页

## 最佳实践

1. **先获取指导**：不确定如何操作时，先调用 `workflow_guide` 获取建议
2. **信任自动验证**：直接调用目标工具，钩子会自动验证必要参数并给出友好提示
3. **先查文档**：调用 API 或查询价格前，先获取相关文档了解结构
4. **逐步细化**：先进行简单查询，再根据结果添加过滤条件
5. **错误处理**：捕获异常，根据错误信息（会列出可用选项）调整参数
6. **明确指定参数**：
   - `huawei_api_request` 必须指定 `account` 和 `service`
   - `query_price` 必须指定 `service`
7. **区域选择**：明确指定 `zone` 参数，避免使用默认值导致的问题
8. **参数完整性**：尽可能在工具调用时提供完整的参数，减少钩子验证失败的可能
9. **利用钩子提示**：如果钩子提示缺少参数，根据提示补充参数后重新调用
