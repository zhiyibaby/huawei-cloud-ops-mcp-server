FROM python:3.11-slim
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY .env.example ./
RUN cp .env.example .env && uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV MCP_HOST=0.0.0.0
ENV MCP_TRANSPORT=http

EXPOSE 8000
ENTRYPOINT ["python", "-m", "huawei_cloud_ops_mcp_server"]
