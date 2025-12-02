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


class _LazyConfigCache(dict[str, Any]):
    """使用 __missing__ 懒加载配置值"""

    def __missing__(self, key: str) -> Any:
        resolver = _CONFIG_RESOLVERS.get(key)
        if resolver is None:
            raise KeyError(key)
        value = resolver()
        self[key] = value
        return value


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
        # 环境变量已在模块加载时通过 load_dotenv 加载，直接获取即可
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
    def _get_key_name(identifier: Optional[str], key_type: str) -> str:
        """根据 identifier 获取密钥名称

        Args:
            identifier: 标识字符串(如 project_id)用于判断使用哪组密钥
            key_type: 密钥类型，'ACCESS_KEY' 或 'SECRET_KEY'

        Returns:
            str: 密钥名称
        """
        account = 'XIAOHEI2018'  # 默认账号

        if identifier:
            identifier_lower = identifier.lower()
            if 'krsk2021' in identifier_lower:
                account = 'KRSK2021'
            elif 'xiaohei2018' in identifier_lower:
                account = 'XIAOHEI2018'

        return f'{account}_CLOUD_{key_type}'

    @staticmethod
    def get_access_key(identifier: Optional[str] = None) -> Optional[str]:
        """获取华为云访问密钥

        Args:
            identifier: 标识字符串(如 project_id)用于判断使用哪组密钥
                       如果包含 'krsk2021'，使用 KRSK2021 密钥
                       如果包含 'xiaohei2018',使用 XIAOHEI2018 密钥
                       默认使用 XIAOHEI2018 密钥
        """
        key_name = HuaweiCloudConfig._get_key_name(identifier, 'ACCESS_KEY')
        value = HuaweiCloudConfig._get_env(key_name)
        if value is None:
            _get_logger().warning(
                f'{key_name} 未设置，请检查环境变量或 .env 文件'
            )
        return value

    @staticmethod
    def get_secret_key(identifier: Optional[str] = None) -> Optional[str]:
        """获取华为云密钥

        Args:
            identifier: 标识字符串,用于判断使用哪组密钥
                       如果包含 'krsk2021'，使用 KRSK2021 密钥
                       如果包含 'xiaohei2018'，使用 XIAOHEI2018 密钥
                       默认使用 XIAOHEI2018 密钥
        """
        key_name = HuaweiCloudConfig._get_key_name(identifier, 'SECRET_KEY')
        value = HuaweiCloudConfig._get_env(key_name)
        if value is None:
            _get_logger().warning(
                f'{key_name} 未设置，请检查环境变量或 .env 文件'
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
