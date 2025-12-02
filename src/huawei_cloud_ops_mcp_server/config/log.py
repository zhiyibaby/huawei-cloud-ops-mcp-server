"""
日志配置模块 - 日志相关配置
"""
from pathlib import Path
from huawei_cloud_ops_mcp_server.config.base import BaseConfigGroup

# 获取项目根目录
_project_root = Path(__file__).resolve().parent.parent.parent


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
