import json
from typing import Optional

from fastmcp import Context
from fastmcp.server.dependencies import get_http_request
from huawei_cloud_ops_mcp_server.common.utils import (
    ToolMetadata, strict_error_handler
)
from huawei_cloud_ops_mcp_server.config.logger import logger
from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import SUPPORTED_SERVICES
from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import PRICE_DOCS


class HuaweiCommonTools:
    """华为云通用工具类"""

    tool_metadatas = {
        'validate_account': ToolMetadata(
            priority=2,
            category='validation',
            timeout=5,
            retryable=False,
        ),
        'elicit_service_info': ToolMetadata(
            priority=1,
            category='elicit',
            timeout=10,
            retryable=False,
        ),
    }

    # 支持的账号列表
    SUPPORTED_ACCOUNTS = ['xiaohei2018', 'krsk2021']

    # 服务名称映射（中文名称 -> 英文服务代码）
    SERVICE_NAME_MAP = {
        'ecs': ['ecs', '弹性云服务器', '云服务器', '服务器'],
        'vpc': ['vpc', '虚拟私有云', '私有云'],
        'rds': ['rds', '关系型数据库', '数据库'],
        'evs': ['evs', '云硬盘', '硬盘'],
        'elb': ['elb', '负载均衡', '负载均衡器'],
        'ims': ['ims', '镜像服务', '镜像'],
        'ces': ['ces', '云监控', '监控'],
        'lts': ['lts', '日志服务', '日志'],
        'obs': ['obs', '对象存储', '存储'],
        'eip': ['eip', '弹性公网ip', '公网ip'],
        'dds': ['dds', '文档数据库'],
        'css': ['css', '云搜索服务'],
        'dcs': ['dcs', '分布式缓存服务', '缓存'],
    }

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
    async def validate_account(ctx: Context, query: str) -> str:
        """验证文本中是否包含有效的账号标识

        此工具用于验证用户输入中是否指定了账号。
        如果请求头中包含 Authorization，则无需指定账号。
        如果未指定账号且请求头中无 Authorization，将使用 elicit 询问用户选择账号。

        Args:
            ctx: FastMCP 上下文对象
            query: 用户的输入文本

        Returns:
            str: 验证结果信息
                - 如果请求头包含 Authorization:返回确认信息
                - 如果找到账号：返回确认信息
                - 如果未找到账号且无 Authorization:通过 elicit 询问用户选择账号

        """
        logger.info(f'验证账号: 分析输入 "{query}"')

        result = []
        result.append('账号验证结果')
        result.append('')

        # 首先检查请求头中是否包含 Authorization
        has_authorization = False
        request = get_http_request()
        if hasattr(request, 'headers'):
            authorization = request.headers.get('Authorization')
            if authorization:
                has_authorization = True
                result.append('检测到请求头中的 Authorization 认证信息')
                result.append('')
                logger.info('账号验证通过: 使用请求头中的 Authorization')

        # 如果没有 Authorization，尝试从输入中提取账号
        if not has_authorization:
            account = HuaweiCommonTools._extract_account(query)
            if account:
                # 找到了账号标识
                result.append(f'检测到账号: {account}')
                result.append('')
                logger.info(f'账号验证通过: 检测到账号 {account}')
            else:
                # 没有找到账号，使用 elicit 询问用户
                available_accounts = ", ".join(
                    HuaweiCommonTools.SUPPORTED_ACCOUNTS
                )

                elicit_result = await ctx.elicit(
                    f"未检测到账号信息，请选择要使用的账号\n\n"
                    f"可用账号: {available_accounts}\n\n"
                    f"请输入账号名称：",
                    response_type=str
                )

                # 检查用户是否接受输入
                if elicit_result.action == 'accept':
                    account = elicit_result.data
                    logger.info(f'用户通过 elicit 选择了账号: {account}')
                else:
                    result.append('用户取消了账号选择')
                    result.append('')
                    return '\n'.join(result)

                # 验证用户输入的账号是否有效
                if account and account in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
                    result.append(f'已选择账号: {account}')
                    result.append('')
                    logger.info(f'账号验证通过: 用户选择账号 {account}')
                else:
                    result.append(f'警告: 选择的账号 "{account}" 不在支持列表中')
                    result.append('')
                    result.append('支持的账号:')
                    for acc in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
                        result.append(f'  - {acc}')
                    result.append('')
                    result.append('请确认账号名称是否正确。')

        result.append('')
        result.append('=' * 60)

        return '\n'.join(result)

    @staticmethod
    def _extract_service(query: str) -> Optional[str]:
        """从文本中提取服务标识

        Args:
            query: 输入文本

        Returns:
            Optional[str]: 找到的服务代码（如 'ecs', 'vpc'），未找到则返回 None
        """
        query_lower = query.lower()
        for service_code, keywords in (
            HuaweiCommonTools.SERVICE_NAME_MAP.items()
        ):
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    return service_code
        return None

    @staticmethod
    def _is_price_query(query: str) -> bool:
        """判断是否为价格查询

        Args:
            query: 输入文本

        Returns:
            bool: 是否为价格查询
        """
        price_keywords = [
            '价格', '费用', '成本', '计费', '定价', 'price', 'cost', 'billing',
            'pricing', 'charge', 'charges', 'fee', 'fees', '多少钱', '多贵'
        ]
        query_lower = query.lower()
        for keyword in price_keywords:
            if keyword.lower() in query_lower:
                return True
        return False

    @staticmethod
    def _is_api_query(query: str) -> bool:
        """判断是否为API查询(实例、资源等)

        Args:
            query: 输入文本

        Returns:
            bool: 是否为API查询
        """
        api_keywords = [
            '实例', '服务器', '资源', '列表', '详情', '查询', '获取',
            'instance', 'server', 'resource', 'list', 'detail', 'query'
        ]
        query_lower = query.lower()
        for keyword in api_keywords:
            if keyword.lower() in query_lower:
                return True
        return False

    @staticmethod
    @strict_error_handler
    async def elicit_service_info(ctx: Context, query: str) -> str:
        """引导用户补全服务信息

        当用户输入不明确（没有明确指定服务类型）时，使用此工具引导用户补全信息。
        例如：用户输入"查询价格"或"查询实例"时，需要明确是查询哪个服务的价格或实例。

        Args:
            ctx: FastMCP 上下文对象
            query: 用户的输入文本

        Returns:
            str: 补全后的服务信息，格式为 JSON 字符串，包含：
                - service: 服务代码(如 'ecs', 'vpc')
                - query_type: 查询类型('price' 或 'api')
                - original_query: 原始查询文本
        """
        logger.info(f'引导补全服务信息: 分析输入 "{query}"')

        result = []
        result.append('服务信息补全结果')
        result.append('')

        # 判断查询类型
        is_price = HuaweiCommonTools._is_price_query(query)
        is_api = HuaweiCommonTools._is_api_query(query)
        query_type = 'unknown'
        if is_price:
            query_type = 'price'
        elif is_api:
            query_type = 'api'

        # 尝试从输入中提取服务
        service = HuaweiCommonTools._extract_service(query)

        # 如果没有明确指定服务，使用 elicit 询问用户
        if not service:
            # 根据查询类型确定可用服务列表
            if query_type == 'price':
                # 价格查询支持的服务
                available_services = sorted(PRICE_DOCS.keys())
                service_type_desc = '价格查询'
            elif query_type == 'api':
                # API查询支持的服务
                available_services = sorted(SUPPORTED_SERVICES)
                service_type_desc = 'API查询'
            else:
                # 未知类型，显示所有服务
                all_services = set(SUPPORTED_SERVICES) | set(PRICE_DOCS.keys())
                available_services = sorted(all_services)
                service_type_desc = '查询'

            # 构建服务选择提示
            service_list = ', '.join(available_services)
            prompt = (
                f'您的查询未明确指定服务类型，请选择要{service_type_desc}的服务\n\n'
                f'可用服务: {service_list}\n\n'
                f'请输入服务名称（如: ecs, vpc, rds 等）：'
            )

            elicit_result = await ctx.elicit(
                prompt,
                response_type=str
            )

            # 检查用户是否接受输入
            if elicit_result.action == 'accept':
                service = elicit_result.data.strip().lower()
                logger.info(f'用户通过 elicit 选择了服务: {service}')

                # 验证服务是否有效
                if query_type == 'price':
                    valid_services = set(PRICE_DOCS.keys())
                elif query_type == 'api':
                    valid_services = set(SUPPORTED_SERVICES)
                else:
                    valid_services = (
                        set(SUPPORTED_SERVICES) | set(PRICE_DOCS.keys())
                    )

                if service not in valid_services:
                    result.append(f'警告: 选择的服务 "{service}" 不在支持列表中')
                    result.append('')
                    result.append(f'支持的{service_type_desc}服务:')
                    for svc in available_services:
                        result.append(f'  - {svc}')
                    result.append('')
                    result.append('请确认服务名称是否正确。')
                    service = None
            else:
                result.append('用户取消了服务选择')
                result.append('')
                service = None

        # 构建返回结果
        if service:
            result.append(f'已确定服务: {service.upper()}')
            result.append(f'查询类型: {query_type}')
            result.append(f'原始查询: {query}')
            result.append('')
            logger.info(
                f'服务信息补全完成: service={service}, '
                f'query_type={query_type}'
            )
        else:
            result.append('未能确定服务信息')
            result.append('')

        result.append('=' * 60)

        # 返回 JSON 格式的结果
        result_dict = {
            'service': service,
            'query_type': query_type,
            'original_query': query,
            'message': '\n'.join(result)
        }
        return json.dumps(
            result_dict,
            separators=(',', ':'),
            ensure_ascii=False
        )
