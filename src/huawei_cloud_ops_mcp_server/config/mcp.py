"""
MCP 配置模块 - MCP 服务器相关配置
"""
from typing import Optional
from huawei_cloud_ops_mcp_server.config.base import BaseConfigGroup, _get_logger


class MCPConfig(BaseConfigGroup):
    """MCP 服务器相关配置"""

    @staticmethod
    def _validate_transport(value: str) -> str:
        """验证 MCP 传输方式"""
        transport = value.lower() if value else 'stdio'
        if transport not in ('stdio', 'http'):
            _get_logger().warning(
                f'不支持的传输方式 {transport},将使用默认值 stdio'
            )
            transport = 'stdio'
        return transport

    @staticmethod
    def get_transport() -> str:
        """获取 MCP 传输方式"""
        return MCPConfig._get_env(
            'MCP_TRANSPORT', 'stdio', MCPConfig._validate_transport
        )

    @staticmethod
    def get_host() -> str:
        """获取 MCP 主机地址"""
        host = MCPConfig._get_env('MCP_HOST')
        if not host or host == 'host':  # 'host' 是无效的占位符值
            transport = MCPConfig.get_transport()
            host = '0.0.0.0' if transport == 'http' else '127.0.0.1'
        return host

    @staticmethod
    def get_port() -> int:
        """获取 MCP 端口号"""
        def _validate_port(value: str) -> int:
            """验证并转换端口号"""
            try:
                port = int(value)
                if port < 1 or port > 65535:
                    _get_logger().warning(
                        f'端口号 {port} 超出有效范围(1-65535),将使用默认值 8000'
                    )
                    return 8000
                return port
            except ValueError:
                _get_logger().warning(
                    f'无效的端口号 {value},将使用默认值 8000'
                )
                return 8000

        return MCPConfig._get_env('MCP_PORT', '8000', _validate_port)

