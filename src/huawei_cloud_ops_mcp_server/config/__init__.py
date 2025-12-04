"""
配置模块 - 统一加载和管理环境变量
采用配置组模式，便于扩展和维护
"""
from typing import Any
from huawei_cloud_ops_mcp_server.config.mcp import MCPConfig
from huawei_cloud_ops_mcp_server.config.logger import LogConfig
from huawei_cloud_ops_mcp_server.config.hw import HuaweiCloudConfig


class Config:
    """主配置类，提供统一的配置访问接口

    使用方式:
        # 方式1: 通过配置组访问（推荐）
        Config.mcp.get_transport()
        Config.log.get_level()
        Config.huawei_cloud.get_access_key(identifier)

        # 方式2: 向后兼容的模块级访问
        from config import MCP_TRANSPORT, MCP_HOST, MCP_PORT
    """
    # 配置组实例
    mcp = MCPConfig()
    log = LogConfig()
    huawei_cloud = HuaweiCloudConfig()


# 向后兼容的配置访问映射
_BACKWARD_COMPAT_MAP: dict[str, str] = {
    'MCP_TRANSPORT': 'mcp.get_transport',
    'MCP_HOST': 'mcp.get_host',
    'MCP_PORT': 'mcp.get_port',
    'LOG_LEVEL': 'log.get_level',
    'LOG_FILE': 'log.get_file',
}


def __getattr__(name: str) -> Any:
    """动态获取配置属性，保持向后兼容"""
    # 向后兼容的配置值访问
    if name in _BACKWARD_COMPAT_MAP:
        attr_path = _BACKWARD_COMPAT_MAP[name]
        parts = attr_path.split('.')
        obj = Config
        for part in parts:
            if part.startswith('get_'):
                # 调用方法
                method = getattr(obj, part)
                return method()
            else:
                # 访问属性
                obj = getattr(obj, part)
        return obj

    # 尝试访问配置组
    if hasattr(Config, name):
        return getattr(Config, name)

    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'"
    )


# 工具配置常量
TOOLS_REQUIRE_ACCOUNT = {'huawei_api_request'}
TOOLS_REQUIRE_SERVICE = {'huawei_api_request', 'query_price'}
