# 工具调用理解文档

本文档说明模型在调用工具时应遵循的规范和最佳实践。

## 工具定义概述

本 MCP 服务器提供了以下工具，用于与华为云 API 进行交互：

### 1. `huawei_api_request` - 统一的华为云 API 请求工具

这是核心工具，用于执行所有华为云 API 调用。

#### 参数说明

- **service** (str, 必需): 服务类型
  - 支持的服务: `ecs`, `vpc`, `rds`, `evs`, `elb`, `ims`
  - 示例: `"ecs"`, `"vpc"`, `"rds"`

- **action** (str, 必需): API 动作/端点路径
  - 如果路径中包含 `{project_id}`，工具会根据 `zone` 参数自动替换为对应区域的项目ID
  - 示例: `"v1/{project_id}/cloudservers/detail"`, `"v2/images"`

- **method** (str, 可选): HTTP 方法
  - 默认值: `"GET"`
  - 可选值: `"GET"`, `"POST"`, `"PUT"`
  - 注意: 当前仅支持 GET 请求方式

- **region** (str, 可选): 区域名称
  - 默认值: `"cn-north-1"`
  - 示例: `"cn-north-1"`, `"cn-east-3"`, `"ap-southeast-1"`
  - 注意: 工具会根据 `zone` 参数自动确定对应的 `region`，此参数主要用于覆盖默认值

- **data** (Dict, 可选): 请求体数据
  - 用于 POST/PUT 请求
  - 示例: `{"server": {"name": "my-server", "imageRef": "image-id"}}`

- **params** (Dict, 可选): 查询参数
  - 用于 GET 请求的 URL 参数
  - 示例: `{"limit": 10, "offset": 0}`

- **zone** (str, 可选): 区域名称
  - 默认值: `"华北-北京一"`
  - 工具会根据 `zone` 自动查找对应的 `project_id` 和 `region`
  - 可用区域包括:
    - `"华北-北京一"`, `"华北-北京四"`, `"华北三"`, `"华北-乌兰察布一"`
    - `"华东-上海一"`, `"华东-上海二"`, `"华东二"`, `"华东-青岛"`
    - `"华南-广州"`, `"华南-广州-友好用户环境"`
    - `"西南-贵阳一"`
    - `"中国-香港"`, `"亚太-曼谷"`, `"亚太-新加坡"`, `"亚太-雅加达"`, `"亚太-马尼拉"`
    - `"非洲-开罗"`, `"非洲-约翰内斯堡"`
    - `"拉美-墨西哥城一"`, `"拉美-墨西哥城二"`, `"拉美-圣地亚哥"`, `"拉美-圣保罗一"`
    - `"中东-利雅得"`, `"土耳其-伊斯坦布尔"`

#### 返回值

- 成功: 返回格式化的 JSON 字符串（包含缩进，中文不转义）
- 失败: 返回错误信息字符串

### 2. `get_huawei_api_docs` - 获取华为云 API 文档说明

用于查询特定服务或所有服务的 API 文档。

#### 参数说明

- **service** (str, 可选): 服务名称
  - 默认值: `"all"`
  - 可选值: `"ecs"`, `"vpc"`, `"rds"`, `"evs"`, `"elb"`, `"ims"`, `"all"`

#### 返回值

- 返回指定服务的 API 文档说明，包括常用端点和请求示例

#### 使用示例

```python
# 获取所有服务的文档
get_huawei_api_docs(service="all")

# 获取 ECS 服务的文档
get_huawei_api_docs(service="ecs")
```

### 3. `list_common_operations` - 列出常用操作示例

返回常用华为云操作的示例说明。

#### 参数说明

- 无参数

#### 返回值

- 返回常用操作的示例列表

#### 使用示例

```python
list_common_operations()
```

## 工具调用规范

### 1. 严格按照工具定义调用

模型在调用工具时，必须：

- **严格按照函数签名传递参数**
  - 参数名称必须完全匹配（区分大小写）
  - 参数类型必须符合定义（str, Dict, 等）
  - 必需参数不能省略

- **理解参数含义**
  - `service`: 必须是支持的服务类型之一
  - `action`: 必须是有效的 API 端点路径
  - `method`: 必须与操作类型匹配（查询用 GET，创建用 POST，更新用 PUT）
  - `zone`: 工具会根据 `zone` 自动查找对应的 `project_id` 和 `region`，无需手动提供 `project_id`

### 2. 参数验证

在调用 `huawei_api_request` 前，应确保：

- `service` 参数是支持的服务之一（`ecs`, `vpc`, `rds`, `evs`, `elb`, `ims`）
- `action` 参数格式正确，如果包含 `{project_id}` 占位符，工具会自动替换（无需手动提供）
- `method` 参数与操作类型匹配（当前仅支持 GET 请求）
- `zone` 参数是有效的区域名称（如果未提供，将使用默认值 `"华北-北京一"`）

### 3. 错误处理

工具调用可能返回错误信息，模型应该：

- 检查返回结果是否包含错误信息
- 如果遇到错误，分析错误原因并采取相应措施
- 常见错误：
  - `project_id 参数未提供` - 检查 `zone` 参数是否正确，确保 `zone` 在配置中存在
  - `不支持的服务类型` - 检查 `service` 参数是否正确
  - `当前仅支持GET请求方式` - 检查 `method` 参数，当前仅支持 GET 请求
  - `API 请求错误` - 检查参数格式和网络连接

### 4. 最佳实践

#### 查询操作流程

1. 如果不确定 API 端点，先调用 `get_huawei_api_docs(service="目标服务")` 获取文档
2. 根据文档确定正确的 `action` 和 `method`
3. 调用 `huawei_api_request` 执行操作
4. 解析返回结果

#### 创建/更新操作流程

1. 查询相关文档了解请求体格式
2. 构建正确的 `data` 参数
3. 使用 `POST`（创建）或 `PUT`（更新）方法
4. 确保所有必需字段都已包含

#### 区域和项目ID处理

- `zone` 参数用于指定区域，工具会根据 `zone` 自动查找对应的 `project_id` 和 `region`
- 如果未提供 `zone` 参数，将使用默认值 `"华北-北京一"`
- 如果 `action` 中包含 `{project_id}` 占位符，工具会自动替换为对应区域的项目ID
- 工具会根据 `zone` 自动设置正确的 `region`，无需手动匹配
- 支持的 `zone` 值包括所有在配置中定义的区域名称（如 `"华北-北京一"`, `"华东-上海一"` 等）

## 常见服务端点参考

### ECS (弹性云服务器)

- 列表: `service="ecs"`, `action="v1/{project_id}/cloudservers/detail"`, `method="GET"`
- 详情: `service="ecs"`, `action="v1/{project_id}/cloudservers/{server_id}"`, `method="GET"`
- 注意: 当前仅支持 GET 请求，创建和删除操作暂不支持

### VPC (虚拟私有云)

- 列表: `service="vpc"`, `action="v1/{project_id}/vpcs"`, `method="GET"`
- 子网列表: `service="vpc"`, `action="v1/{project_id}/subnets"`, `method="GET"`
- 注意: 当前仅支持 GET 请求，创建操作暂不支持

### RDS (关系型数据库)

- 列表: `service="rds"`, `action="v3/{project_id}/instances"`, `method="GET"`
- 注意: 当前仅支持 GET 请求，创建操作暂不支持

### EVS (云硬盘)

- 列表: `service="evs"`, `action="v2/{project_id}/cloudvolumes"`, `method="GET"`
- 注意: 当前仅支持 GET 请求，创建操作暂不支持

### ELB (弹性负载均衡)

- 列表: `service="elb"`, `action="v2/{project_id}/elb/loadbalancers"`, `method="GET"`
- 注意: 当前仅支持 GET 请求，创建操作暂不支持

### IMS (镜像服务)

- 列表: `service="ims"`, `action="v2/images"`, `method="GET"`

## 注意事项

1. **区域和项目ID**: 工具会根据 `zone` 参数自动查找对应的 `project_id` 和 `region`，无需手动提供 `project_id`
2. **默认区域**: 如果未提供 `zone` 参数，将使用默认值 `"华北-北京一"`
3. **HTTP 方法限制**: 当前仅支持 GET 请求方式，POST/PUT/DELETE 请求暂不支持
4. **认证信息**: 工具会自动使用环境变量中的认证信息，无需在调用中传递
5. **占位符替换**: `action` 中的 `{project_id}` 会自动替换为对应区域的项目ID，无需手动处理
6. **返回值格式**: 返回值是 JSON 字符串，需要解析才能使用其中的数据
7. **区域名称**: 使用完整的中文区域名称（如 `"华北-北京一"`），工具会进行模糊匹配

## 总结

模型在调用工具时，应该：

1. 严格按照工具定义传递参数
2. 理解每个参数的含义和格式要求
3. 在不确定时先查询文档
4. 正确处理错误和异常情况
5. 遵循最佳实践和常见操作流程

通过遵循这些规范，可以确保工具调用的准确性和可靠性。
