# 华为云运维 MCP 服务器

基于 Model Context Protocol (MCP) 的华为云 API 调用服务器，为 AI 助手提供华为云资源查询、价格查询和管理能力。

## 功能特性

- **API 调用**: 支持查询和管理华为云资源（ECS、VPC、RDS、EVS、ELB、OBS、EIP、DDS、CSS、DCS、CES 等）
- **价格查询**: 支持查询华为云服务价格信息，支持多条件过滤
- **工作流指导**: 智能分析用户查询，提供工具调用建议
- **多区域支持**: 支持华为云全球多个区域，自动处理 project_id 和 region 映射
- **文档集成**: 内置 API 文档和价格结构文档，支持快速查询

## 主要工具

### API 工具
- `huawei_api_request`: 执行华为云 API 请求
- `get_huawei_api_docs`: 获取华为云 API 文档

### 价格工具
- `query_price`: 查询服务价格信息（支持多条件过滤）
- `get_price_structure_doc`: 获取价格数据结构文档

### 工作流工具
- `workflow_guide`: 根据用户查询提供工具调用建议
- `prompt_understanding`: 获取工具调用理解文档

## 安装

### 前置要求
- Python >= 3.11
- 华为云账号及访问密钥 (AK/SK)

### 安装步骤

1. 安装依赖：
```bash
# 使用 uv (推荐)
uv sync
# 或使用 pip
pip install -e .
```

2. 配置环境变量（创建 `.env` 文件）：
```env
HUAWEI_CLOUD_ACCESS_KEY=your_access_key
HUAWEI_CLOUD_SECRET_KEY=your_secret_key
# MCP 传输方式：stdio（默认）或 http（用于 Docker）
MCP_TRANSPORT=http
# 日志配置（可选）
# LOG_LEVEL=INFO
# LOG_FILE=logs/app.log
```

## 使用方法

### Docker 运行（推荐）

1. 构建镜像：
```bash
docker build -t huawei-cloud-ops-mcp-server .
```

2. 运行容器：
```bash
docker run -d --rm \
  -e HUAWEI_CLOUD_ACCESS_KEY=your_access_key \
  -e HUAWEI_CLOUD_SECRET_KEY=your_secret_key \
  -e MCP_TRANSPORT=http \
  -e MCP_HOST=0.0.0.0 \
  -p 8000:8000 \
  huawei-cloud-ops-mcp-server
```

**注意**：`MCP_HOST` 和 `MCP_TRANSPORT` 在 Dockerfile 中已默认设置为 `0.0.0.0` 和 `http`，通常无需手动指定。如果遇到线程限制问题，可以使用 `--ulimit nproc=4096` 参数。

3. MCP 客户端配置（HTTP 传输）：
```json
{
  "mcpServers": {
    "huawei-cloud-ops": {
      "url": "http://localhost:8000"
    }
  }
}
```

### 本地运行

1. 启动服务器：
```bash
python -m huawei_cloud_ops_mcp_server
linux: nohup uv run python -m huawei_cloud_ops_mcp_server > /dev/null 2>&1 </dev/null &
```

2. MCP 客户端配置（stdio 传输）：
```json
{
  "mcpServers": {
    "huawei-cloud-ops": {
      "command": "python",
      "args": ["-m", "huawei_cloud_ops_mcp_server"]
    }
  }
}
```

## 注意事项

1. 当前仅支持 GET 请求，POST/PUT/DELETE 暂不支持
2. 区域名称使用完整中文（如 `"华北-北京一"`），支持模糊匹配
3. API 返回 JSON 字符串格式
4. 日志文件默认保存在 `logs/app.log`

## 相关链接

- [华为云 API 文档](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212668.html)
- [Model Context Protocol 规范](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://github.com/jlowin/fastmcp)
