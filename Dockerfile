# 使用 Python 3.11 slim 作为基础镜像
FROM python:3.11-slim as builder

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目配置文件
COPY pyproject.toml uv.lock ./

# 使用 uv 安装依赖到虚拟环境
RUN uv sync --frozen

# 运行阶段
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制项目源代码
COPY src/ ./src/

# 设置环境变量，确保使用虚拟环境中的 Python
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 暴露端口（如果需要 HTTP 传输）
EXPOSE 8000

# 设置入口点
ENTRYPOINT ["python", "-m", "huawei_cloud_ops_mcp_server"]
