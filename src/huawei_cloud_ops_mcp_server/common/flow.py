from typing import Callable, Optional
from fastmcp import Context
from huawei_cloud_ops_mcp_server.config.logger import logger
from huawei_cloud_ops_mcp_server.tools.common_tools import HuaweiCommonTools
from huawei_cloud_ops_mcp_server.config import (
    TOOLS_REQUIRE_ACCOUNT, TOOLS_REQUIRE_SERVICE
)
from fastmcp.server.dependencies import get_http_request


def _extract_from_args(
    args: dict, key: str, extract_func: Callable[[str], Optional[str]]
) -> Optional[str]:
    """从工具参数中提取值（账号或服务）

    Args:
        args: 工具参数字典
        key: 要提取的键名（如 'account' 或 'service'）
        extract_func: 提取函数

    Returns:
        Optional[str]: 提取到的值，未找到返回 None
    """
    if key in args and args[key]:
        return args[key]

    for value in args.values():
        if isinstance(value, str):
            result = extract_func(value)
            if result:
                return result
    return None


def _check_authorization() -> bool:
    """检查请求头中是否包含 Authorization"""
    try:
        request = get_http_request()
        return bool(
            hasattr(request, 'headers')
            and request.headers.get('Authorization')
        )
    except Exception:
        return False


def _extract_from_context(
    ctx: Optional[Context],
    key: str,
    extract_func: Callable[[str], Optional[str]]
) -> Optional[str]:
    """从 context 中提取值（账号或服务）

    Args:
        ctx: FastMCP Context 对象
        key: 要提取的键名
        extract_func: 提取函数

    Returns:
        Optional[str]: 提取到的值，未找到返回 None
    """
    if not ctx:
        return None

    # 从 metadata 中提取
    try:
        metadata = getattr(ctx, 'metadata', {})
        if metadata and key in metadata:
            return metadata[key]
    except Exception as e:
        logger.debug(f'从 context.metadata 提取 {key} 失败: {e}')

    # 从 request_params 中提取
    try:
        request_params = getattr(ctx, 'request_params', {})
        for value in request_params.values():
            if isinstance(value, str):
                result = extract_func(value)
                if result:
                    return result
    except Exception as e:
        logger.debug(f'从 context.request_params 提取 {key} 失败: {e}')

    return None


async def validate_tool_params(
    tool_name: str, args: dict, ctx: Optional[Context] = None
) -> None:
    """验证工具参数

    Args:
        tool_name: 工具名称
        args: 工具参数字典
        ctx: FastMCP Context 对象

    Raises:
        UserInputRequiredError: 缺少必要参数且无法自动补全时抛出
    """
    logger.info(f'验证工具参数: tool={tool_name}, args={args}')

    # 验证账号
    if tool_name in TOOLS_REQUIRE_ACCOUNT:
        account = None
        has_authorization = _check_authorization()

        if has_authorization:
            account = (
                args.get('account')
                or HuaweiCommonTools.SUPPORTED_ACCOUNTS[0]
            )
            action = (
                '设置占位账号'
                if not args.get('account')
                else '保留参数中的账号'
            )
            logger.info(
                f'使用 Authorization 请求头，{action}: {account}'
            )
        else:
            # 尝试从 context 提取
            account = _extract_from_context(
                ctx, 'account', HuaweiCommonTools._extract_account
            )
            if account:
                logger.info(f'从 context 中提取到账号: {account}')

            # 尝试从 args 提取
            if not account:
                account = _extract_from_args(
                    args, 'account', HuaweiCommonTools._extract_account
                )

            # 验证账号
            if not account:
                accounts = ', '.join(HuaweiCommonTools.SUPPORTED_ACCOUNTS)
                raise UserInputRequiredError(
                    f'工具 "{tool_name}" 需要账号信息。\n\n'
                    f'未检测到账号信息，请选择要使用的账号。\n\n'
                    f'可用账号: {accounts}\n\n'
                    f'请在参数中指定账号，或在查询中包含账号名称。'
                )

            if account not in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
                accounts = ', '.join(HuaweiCommonTools.SUPPORTED_ACCOUNTS)
                raise ValueError(
                    f'账号 "{account}" 不在支持列表中。\n\n'
                    f'可用账号: {accounts}'
                )

        args['account'] = account
        logger.info(f'账号验证通过并已补全到参数: {account}')

    # 验证服务
    if tool_name in TOOLS_REQUIRE_SERVICE:
        service = _extract_from_context(
            ctx, 'service', HuaweiCommonTools._extract_service
        )
        if service:
            logger.info(f'从 context 中提取到服务: {service}')

        if not service:
            service = _extract_from_args(
                args, 'service', HuaweiCommonTools._extract_service
            )

        if not service:
            from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import (
                SUPPORTED_SERVICES
            )
            from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
                PRICE_DOCS
            )

            if tool_name == 'query_price':
                available_services = sorted(PRICE_DOCS.keys())
                service_type_desc = '价格查询'
            else:
                available_services = sorted(SUPPORTED_SERVICES)
                service_type_desc = 'API查询'

            service_list = ', '.join(available_services)
            raise UserInputRequiredError(
                f'工具 "{tool_name}" 需要服务信息。\n\n'
                f'未检测到服务类型，请指定要{service_type_desc}的服务。\n\n'
                f'可用服务: {service_list}\n\n'
                f'请在参数中指定服务，或在查询中包含服务名称(如: ecs, vpc, rds 等).'
            )

        args['service'] = service
        logger.info(f'服务验证通过并已补全到参数: {service}')