from typing import Optional
from huawei_cloud_ops_mcp_server.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.logger import logger


class HuaweiCommonTools:
    """华为云通用工具类"""

    tool_metadatas = {
        'validate_account': ToolMetadata(
            priority=2,
            category='validation',
            timeout=5,
            retryable=False,
        ),
    }

    # 支持的账号列表
    SUPPORTED_ACCOUNTS = ['xiaohei2018', 'krsk2021']

    @staticmethod
    def _extract_account(text: str) -> Optional[str]:
        """从文本中提取账号标识

        Args:
            text: 输入文本

        Returns:
            Optional[str]: 找到的账号标识，未找到则返回 None
        """
        text_lower = text.lower()
        for account in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
            if account.lower() in text_lower:
                return account
        return None

    @staticmethod
    @strict_error_handler
    async def validate_account(query: str) -> str:
        """验证文本中是否包含有效的账号标识

        此工具用于验证用户输入中是否指定了账号。
        如果未指定账号，将返回提示信息要求用户指定。

        Args:
            query: 用户的输入文本

        Returns:
            str: 验证结果信息
                - 如果找到账号：返回确认信息
                - 如果未找到账号：返回提示用户指定账号的信息

        示例:
            # 包含账号
            validate_account("查询 xiaohei2018 的 ECS 实例")
            # 返回: "检测到账号: xiaohei2018"

            # 不包含账号
            validate_account("查询 ECS 实例列表")
            # 返回: "请指定要查询的账号..."
        """
        logger.info(f'验证账号: 分析输入 "{query}"')
        # 尝试从输入中提取账号
        account = HuaweiCommonTools._extract_account(query)
        result = []
        result.append('=' * 60)
        result.append('账号验证结果')
        result.append('=' * 60)
        result.append('')

        if account:
            # 找到了账号标识
            result.append(f'✓ 检测到账号: {account}')
            result.append('')
            result.append('可以继续执行操作。')
            logger.info(f'账号验证通过: {account}')
        else:
            # 没有找到账号
            result.append('✗ 未检测到账号标识')
            result.append('')
            result.append('请指定要使用的账号:')
            result.append('')
            result.append('支持的账号:')
            for acc in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
                result.append(f'  - {acc}')
            result.append('')
            result.append('请在您的请求中明确指定账号，例如:')
            result.append('  "查询 xiaohei2018 的 ECS 实例"')
            result.append('  "获取 krsk2021 的服务器列表"')
            logger.warning(f'输入缺少账号标识: {query}')

        result.append('')
        result.append('=' * 60)

        return '\n'.join(result)
