"""
华为云配置模块 - 华为云相关配置
"""
from typing import Optional
from huawei_cloud_ops_mcp_server.config.base import (
    BaseConfigGroup, _get_logger
)


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
