"""
配置模块 - 统一加载和管理环境变量
"""
import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).parent.parent.parent
_env_file = _project_root / '.env'

load_dotenv(dotenv_path=_env_file)

# 初始化日志（延迟导入避免循环依赖）
_logger = None

# 导出常用的配置变量，方便其他模块使用
HUAWEI_CLOUD_ACCESS_KEY = os.getenv('HUAWEI_CLOUD_ACCESS_KEY')
HUAWEI_CLOUD_SECRET_KEY = os.getenv('HUAWEI_CLOUD_SECRET_KEY')


def _get_logger():
    """延迟初始化日志记录器"""
    global _logger
    if _logger is None:
        from huawei_cloud_ops_mcp_server.logger import logger
        _logger = logger
    return _logger


# MCP 传输方式配置，支持 'stdio' 或 'http'，默认为 'stdio'
MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'stdio').lower()
MCP_HOST = os.getenv('MCP_HOST')
MCP_HOST = MCP_HOST if MCP_HOST not in (None, '') else '127.0.0.1'
if MCP_TRANSPORT not in ('stdio', 'http'):
    _get_logger().warning(
        f'不支持的传输方式 {MCP_TRANSPORT}，将使用默认值 stdio'
    )
    MCP_TRANSPORT = 'stdio'

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', str(_project_root / 'logs' / 'app.log'))
