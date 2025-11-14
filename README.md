# 华为云运维 MCP 服务器

一个基于 Model Context Protocol (MCP) 的华为云 API 调用服务器，为 AI 助手提供华为云资源查询和管理能力。

## 功能特性

- **MCP 协议支持**: 基于 FastMCP 框架，兼容 MCP 标准协议
- **多服务支持**: 支持 ECS、VPC、RDS、EVS、ELB、OBS、EIP、DDS、CSS、DCS 等多个华为云服务
- **多区域支持**: 支持华为云全球多个区域，自动处理 project_id 和 region 映射
- **API 文档集成**: 内置常用 API 文档，支持快速查询
- **安全认证**: 使用华为云 AK/SK 认证，支持环境变量配置
- **工具自动发现**: 自动加载和注册工具，支持优先级配置

## 支持的服务

| 服务 | 说明 | 文档 |
|------|------|------|
| ECS | 弹性云服务器 | [ECS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/ECS.md) |
| VPC | 虚拟私有云 | [VPC.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/VPC.md) |
| RDS | 关系型数据库 | [RDS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/RDS.md) |
| EVS | 云硬盘 | [EVS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/EVS.md) |
| ELB | 弹性负载均衡 | [ELB.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/ELB.md) |
| OBS | 对象存储服务 | [OBS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/OBS.md) |
| EIP | 弹性公网IP | [EIP.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/EIP.md) |
| DDS | 文档数据库 | [DDS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/DDS.md) |
| CSS | 云搜索服务 | [CSS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/CSS.md) |
| DCS | 分布式缓存服务 | [DCS.md](src/huawei_cloud_ops_mcp_server/huaweicloud/apidocs/DCS.md) |

## 安装

### 前置要求

- Python >= 3.11
- 华为云账号及访问密钥 (AK/SK)

### 安装步骤

1. 克隆项目：
```bash
git clone <repository-url>
cd huawei-cloud-ops-mcp-server
```

2. 安装依赖：
```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

3. 配置环境变量：
在项目根目录创建 `.env` 文件：
```env
HUAWEI_CLOUD_ACCESS_KEY=your_access_key
HUAWEI_CLOUD_SECRET_KEY=your_secret_key
# MCP 传输方式，可选值：stdio（默认，用于 Docker/命令行运行）或 http（用于 HTTP 服务）
MCP_TRANSPORT=stdio
```

## 使用方法

### 使用 Docker 运行（推荐）

1. 构建 Docker 镜像：
```bash
docker build -t huawei-cloud-ops-mcp-server .
```

2. 运行容器（需要设置环境变量）：
   
   **使用 stdio 传输（推荐，用于 MCP 客户端）：**
   ```bash
   docker run -i --rm \
     -e HUAWEI_CLOUD_ACCESS_KEY=your_access_key \
     -e HUAWEI_CLOUD_SECRET_KEY=your_secret_key \
     -e MCP_TRANSPORT=stdio \
     huawei-cloud-ops-mcp-server
   ```
   
   **使用 HTTP 传输（需要端口映射）：**
   ```bash
   docker run -d --rm \
     -e HUAWEI_CLOUD_ACCESS_KEY=your_access_key \
     -e HUAWEI_CLOUD_SECRET_KEY=your_secret_key \
     -e MCP_TRANSPORT=http \
     -p 8000:8000 \
     huawei-cloud-ops-mcp-server
   ```
   如需前台输出日志，可移除 `-d` 参数。

3. 在 MCP 客户端中配置（使用 Docker，stdio 传输）：
```json
{
  "mcpServers": {
    "huawei-cloud-ops": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "HUAWEI_CLOUD_ACCESS_KEY=${HUAWEI_CLOUD_ACCESS_KEY}",
        "-e", "HUAWEI_CLOUD_SECRET_KEY=${HUAWEI_CLOUD_SECRET_KEY}",
        "-e", "MCP_TRANSPORT=stdio",
        "huawei-cloud-ops-mcp-server"
      ]
    }
  }
}
```

### 作为 MCP 服务器运行（本地）

1. 启动服务器：
```bash
python -m huawei_cloud_ops_mcp_server
```

2. 在 MCP 客户端中配置：
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

## 项目结构

```
huawei-cloud-ops-mcp-server/
├── src/
│   └── huawei_cloud_ops_mcp_server/
│       ├── __init__.py
│       ├── __main__.py          # 入口文件
│       ├── config.py            # 配置管理
│       ├── server.py            # MCP 服务器主逻辑
│       ├── utils.py             # 工具函数
│       ├── tools/               # 工具模块
│       │   ├── __init__.py
│       │   └── api_tools.py     # API 调用工具
│       └── huaweicloud/         # 华为云相关
│           ├── config.py        # 华为云配置
│           ├── signer.py        # 签名工具
│           ├── utils.py         # 工具函数
│           ├── apidocs/         # API 文档
│           └── static/         # 静态文档
├── pyproject.toml               # 项目配置
├── README.md                    # 本文档
├── Dockerfile                   # Docker 镜像构建文件
└── .env                         # 环境变量（需自行创建）
```

## 注意事项

1. **HTTP 方法限制**: 当前仅支持 GET 请求，POST/PUT/DELETE 请求暂不支持
2. **认证信息**: 确保 `.env` 文件中的 AK/SK 配置正确
3. **区域名称**: 使用完整的中文区域名称（如 `"华北-北京一"`），工具会进行模糊匹配
4. **project_id 占位符**: `action` 中的 `{project_id}` 会自动替换为对应区域的项目ID
5. **返回值格式**: API 返回的是 JSON 字符串，需要解析才能使用其中的数据

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [华为云 API 文档](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212668.html)
- [Model Context Protocol 规范](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://github.com/jlowin/fastmcp)
