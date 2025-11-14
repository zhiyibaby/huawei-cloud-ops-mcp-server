"""
配置模块 - 统一加载和管理环境变量
"""
import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).parent.parent.parent
_env_file = _project_root / '.env'

load_dotenv(dotenv_path=_env_file)

# 导出常用的配置变量，方便其他模块使用
HUAWEI_CLOUD_ACCESS_KEY = os.getenv('HUAWEI_CLOUD_ACCESS_KEY')
HUAWEI_CLOUD_SECRET_KEY = os.getenv('HUAWEI_CLOUD_SECRET_KEY')

# MCP 传输方式配置，支持 'stdio' 或 'http'，默认为 'stdio'
MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'stdio').lower()
if MCP_TRANSPORT not in ('stdio', 'http'):
    print(f'警告: 不支持的传输方式 {MCP_TRANSPORT}，将使用默认值 stdio')
    MCP_TRANSPORT = 'stdio'
