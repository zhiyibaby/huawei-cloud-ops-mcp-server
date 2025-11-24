"""
配置模块 - 统一加载和管理环境变量
"""
import os
from pathlib import Path
from typing import Optional, Callable, Any
from dotenv import load_dotenv

_project_root = Path(__file__).parent.parent.parent
_env_file = _project_root / '.env'

load_dotenv(dotenv_path=_env_file)

# 初始化日志(延迟导入避免循环依赖)
_logger = None


def _get_logger():
    """延迟初始化日志记录器"""
    global _logger
    if _logger is None:
        from huawei_cloud_ops_mcp_server.logger import logger
        _logger = logger
    return _logger


class Config:
    """动态配置管理器"""

    @staticmethod
    def _get_env(
        key: str,
        default: Any = None,
        validator: Optional[Callable[[str], Any]] = None
    ) -> Any:
        """
        动态获取环境变量

        Args:
            key: 环境变量键名
            default: 默认值
            validator: 可选的验证/转换函数

        Returns:
            配置值
        """
        value = os.getenv(key, default)
        if validator:
            value = validator(value)
        return value

    @staticmethod
    def _validate_mcp_transport(value: str) -> str:
        """验证 MCP 传输方式"""
        transport = value.lower() if value else 'stdio'
        if transport not in ('stdio', 'http'):
            _get_logger().warning(
                f'不支持的传输方式 {transport},将使用默认值 stdio'
            )
            transport = 'stdio'
        return transport

    @staticmethod
    def _get_mcp_host() -> str:
        """动态获取 MCP 主机地址"""
        host = os.getenv('MCP_HOST')
        if host in (None, '', 'host'):
            transport = Config.get_mcp_transport()
            host = '0.0.0.0' if transport == 'http' else '127.0.0.1'
        return host

    @staticmethod
    def get_mcp_transport() -> str:
        """获取 MCP 传输方式"""
        return Config._get_env(
            'MCP_TRANSPORT', 'stdio', Config._validate_mcp_transport
        )

    @staticmethod
    def get_mcp_host() -> str:
        """获取 MCP 主机地址"""
        return Config._get_mcp_host()

    @staticmethod
    def get_mcp_port() -> int:
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

    @staticmethod
    def get_log_level() -> str:
        """获取日志级别"""
        return Config._get_env('LOG_LEVEL', 'INFO')

    @staticmethod
    def get_log_file() -> str:
        """获取日志文件路径"""
        default_path = str(_project_root / 'logs' / 'app.log')
        return Config._get_env('LOG_FILE', default_path)

    @staticmethod
    def get_huawei_cloud_access_key() -> Optional[str]:
        """获取华为云访问密钥"""
        return Config._get_env('HUAWEI_CLOUD_ACCESS_KEY')

    @staticmethod
    def get_huawei_cloud_secret_key() -> Optional[str]:
        """获取华为云密钥"""
        return Config._get_env('HUAWEI_CLOUD_SECRET_KEY')


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
        return config_map[name]()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
