"""
配置基类模块 - 提供通用的配置组基类和工具函数
"""
import os
from pathlib import Path
from typing import Optional, Callable, Any
from dotenv import load_dotenv

# 项目根目录和环境变量文件
_project_root = Path(__file__).resolve().parent.parent.parent
_env_file = _project_root / '.env'
_env_loaded = load_dotenv(dotenv_path=_env_file, override=False)
_logger = None


def _get_logger():
    """延迟初始化日志记录器"""
    global _logger
    if _logger is None:
        from huawei_cloud_ops_mcp_server.config.logger import logger
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
