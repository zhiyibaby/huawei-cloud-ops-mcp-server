"""
配置模块 - 统一加载和管理环境变量
采用配置组模式，便于扩展和维护
"""
from typing import Any, Callable, Optional
from huawei_cloud_ops_mcp_server.config.base import BaseConfigGroup
from huawei_cloud_ops_mcp_server.config.mcp import MCPConfig
from huawei_cloud_ops_mcp_server.config.logger import LogConfig
from huawei_cloud_ops_mcp_server.config.hw import HuaweiCloudConfig


class _LazyConfigCache(dict[str, Any]):
    """使用 __missing__ 懒加载配置值"""

    def __missing__(self, key: str) -> Any:
        resolver = _CONFIG_RESOLVERS.get(key)
        if resolver is None:
            raise KeyError(key)
        value = resolver()
        self[key] = value
        return value


class Config:
    """主配置类，提供统一的配置访问接口"""
    # 配置组实例
    mcp = MCPConfig()
    log = LogConfig()
    huawei_cloud = HuaweiCloudConfig()

    @staticmethod
    def get_mcp_transport() -> str:
        return MCPConfig.get_transport()

    @staticmethod
    def get_mcp_host() -> str:
        return MCPConfig.get_host()

    @staticmethod
    def get_mcp_port() -> int:
        return MCPConfig.get_port()

    @staticmethod
    def get_log_level() -> str:
        return LogConfig.get_level()

    @staticmethod
    def get_log_file() -> str:
        return LogConfig.get_file()

    @staticmethod
    def get_huawei_cloud_access_key(
        identifier: Optional[str] = None
    ) -> Optional[str]:
        return HuaweiCloudConfig.get_access_key(identifier)

    @staticmethod
    def get_huawei_cloud_secret_key(
        identifier: Optional[str] = None
    ) -> Optional[str]:
        return HuaweiCloudConfig.get_secret_key(identifier)


# 可复用的配置获取映射
_CONFIG_RESOLVERS: dict[str, Callable[[], Any]] = {
    'MCP_TRANSPORT': Config.get_mcp_transport,
    'MCP_HOST': Config.get_mcp_host,
    'MCP_PORT': Config.get_mcp_port,
    'LOG_LEVEL': Config.get_log_level,
    'LOG_FILE': Config.get_log_file
}
_config_cache = _LazyConfigCache()


# 使用 __getattr__ 实现动态属性访问,保持向后兼容
def __getattr__(name: str) -> Any:
    """动态获取配置属性"""
    try:
        return _config_cache[name]
    except KeyError as exc:
        raise AttributeError(
            f"module '{__name__}' has no attribute '{name}'"
        ) from exc


# 导出所有配置类和主配置类
__all__ = [
    'BaseConfigGroup',
    'MCPConfig',
    'LogConfig',
    'HuaweiCloudConfig',
    'Config',
]
