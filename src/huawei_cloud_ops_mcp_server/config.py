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
