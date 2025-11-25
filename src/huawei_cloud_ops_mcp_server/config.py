"""
配置模块 - 统一加载和管理环境变量
采用配置组模式，便于扩展和维护
"""
import os
from pathlib import Path
from typing import Optional, Callable, Any
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
_env_file = _project_root / '.env'
_env_loaded = load_dotenv(dotenv_path=_env_file, override=False)

if not _env_file.exists():
    import logging
    logging.warning(
        f'.env 文件不存在: {_env_file}，将仅从系统环境变量读取配置'
    )
elif _env_loaded:
    import logging
    logging.debug(f'成功加载 .env 文件: {_env_file}')


_logger = None
_config_cache: dict[str, Any] = {}


def _get_logger():
    """延迟初始化日志记录器"""
    global _logger
    if _logger is None:
        from huawei_cloud_ops_mcp_server.logger import logger
        _logger = logger
    return _logger


class BaseConfigGroup:
    """配置组基类，提供通用的环境变量获取方法"""

    @staticmethod
    def _get_env(
        key: str,
        default: Any = None,
        validator: Optional[Callable[[str], Any]] = None
    ) -> Any:
        value = os.getenv(key)
        if value is None and default is None:
            load_dotenv(dotenv_path=_env_file, override=False)
            value = os.getenv(key)
        if value is None:
            value = default

        if validator:
            value = validator(value)
        return value


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
        host = os.getenv('MCP_HOST')
        if host in (None, '', 'host'):
            transport = MCPConfig.get_transport()
            host = '0.0.0.0' if transport == 'http' else '127.0.0.1'
        return host

    @staticmethod
    def get_port() -> int:
        """获取 MCP 端口号"""
        port_str = os.getenv('MCP_PORT', '8000')
        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                _get_logger().warning(
                    f'端口号 {port} 超出有效范围(1-65535),将使用默认值 8000'
                )
                return 8000
            return port
        except ValueError:
            _get_logger().warning(
                f'无效的端口号 {port_str},将使用默认值 8000'
            )
            return 8000


class LogConfig(BaseConfigGroup):
    """日志相关配置"""

    @staticmethod
    def get_level() -> str:
        """获取日志级别"""
        return LogConfig._get_env('LOG_LEVEL', 'INFO')

    @staticmethod
    def get_file() -> str:
        """获取日志文件路径"""
        default_path = str(_project_root / 'logs' / 'app.log')
        return LogConfig._get_env('LOG_FILE', default_path)


class HuaweiCloudConfig(BaseConfigGroup):
    """华为云相关配置"""

    @staticmethod
    def get_access_key() -> Optional[str]:
        """获取华为云访问密钥"""
        value = HuaweiCloudConfig._get_env('HUAWEI_CLOUD_ACCESS_KEY')
        if value is None:
            _get_logger().warning(
                'HUAWEI_CLOUD_ACCESS_KEY 未设置，请检查环境变量或 .env 文件'
            )
        return value

    @staticmethod
    def get_secret_key() -> Optional[str]:
        """获取华为云密钥"""
        value = HuaweiCloudConfig._get_env('HUAWEI_CLOUD_SECRET_KEY')
        if value is None:
            _get_logger().warning(
                'HUAWEI_CLOUD_SECRET_KEY 未设置，请检查环境变量或 .env 文件'
            )
        return value


class Config:
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
    def get_huawei_cloud_access_key() -> Optional[str]:
        return HuaweiCloudConfig.get_access_key()

    @staticmethod
    def get_huawei_cloud_secret_key() -> Optional[str]:
        return HuaweiCloudConfig.get_secret_key()


# 使用 __getattr__ 实现动态属性访问,保持向后兼容
def __getattr__(name: str) -> Any:
    """动态获取配置属性"""
    config_map = {
        'MCP_TRANSPORT': Config.get_mcp_transport,
        'MCP_HOST': Config.get_mcp_host,
        'MCP_PORT': Config.get_mcp_port,
        'LOG_LEVEL': Config.get_log_level,
        'LOG_FILE': Config.get_log_file,
        'HUAWEI_CLOUD_ACCESS_KEY': Config.get_huawei_cloud_access_key,
        'HUAWEI_CLOUD_SECRET_KEY': Config.get_huawei_cloud_secret_key,
    }
    if name in config_map:
        if name not in _config_cache:
            _config_cache[name] = config_map[name]()
        return _config_cache[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
