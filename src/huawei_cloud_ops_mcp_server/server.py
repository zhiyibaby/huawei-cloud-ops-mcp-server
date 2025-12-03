import asyncio
import functools
from typing import Any, Callable, Optional

from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_request

from huawei_cloud_ops_mcp_server.config import (
    MCP_TRANSPORT, MCP_HOST, MCP_PORT
)
from huawei_cloud_ops_mcp_server.common.register import (
    load_tools, load_resources
)
from huawei_cloud_ops_mcp_server.config.logger import logger
from huawei_cloud_ops_mcp_server.tools.common_tools import (
    HuaweiCommonTools, UserInputRequiredError
)


# 需要账号验证的工具列表
TOOLS_REQUIRE_ACCOUNT = {'huawei_api_request'}
# 需要服务验证的工具列表
TOOLS_REQUIRE_SERVICE = {'huawei_api_request', 'query_price'}


def _extract_account_from_args(tool_name: str, args: dict) -> Optional[str]:
    """从工具参数中提取账号

    Args:
        tool_name: 工具名称
        args: 工具参数字典

    Returns:
        Optional[str]: 提取到的账号，未找到返回 None
    """
    # 如果参数中已经有 account，直接返回
    if 'account' in args and args['account']:
        return args['account']

    # 尝试从其他参数中提取账号（如 query 参数）
    for key, value in args.items():
        if isinstance(value, str):
            account = HuaweiCommonTools._extract_account(value)
            if account:
                return account

    return None


def _extract_service_from_args(tool_name: str, args: dict) -> Optional[str]:
    """从工具参数中提取服务

    Args:
        tool_name: 工具名称
        args: 工具参数字典

    Returns:
        Optional[str]: 提取到的服务代码，未找到返回 None
    """
    # 如果参数中已经有 service，直接返回
    if 'service' in args and args['service']:
        return args['service']

    # 尝试从其他参数中提取服务（如 query 参数）
    for key, value in args.items():
        if isinstance(value, str):
            service = HuaweiCommonTools._extract_service(value)
            if service:
                return service

    return None


def _check_authorization() -> bool:
    """检查请求头中是否包含 Authorization

    Returns:
        bool: 是否包含有效的 Authorization
    """
    try:
        request = get_http_request()
        if hasattr(request, 'headers'):
            authorization = request.headers.get('Authorization')
            if authorization:
                return True
    except Exception:
        # 如果无法获取请求对象（stdio模式），返回 False
        pass
    return False


async def validate_tool_params(
    tool_name: str, args: dict, ctx: Optional[Context] = None
) -> None:
    """验证工具参数

    Args:
        tool_name: 工具名称
        args: 工具参数字典
        ctx: FastMCP Context 对象（可选）

    Raises:
        UserInputRequiredError: 缺少必要参数且无法自动补全时抛出
    """
    logger.info(f'验证工具参数: tool={tool_name}, args={args}')

    # 1. 验证账号（仅对需要账号的工具）
    if tool_name in TOOLS_REQUIRE_ACCOUNT:
        # 检查是否有 Authorization 头
        has_authorization = _check_authorization()

        if has_authorization:
            # 有 Authorization 请求头，直接使用请求头中的认证信息
            # 在 HuaweiCloudClient.request 中会自动使用请求头的认证信息
            # 如果参数中没有 account，给一个占位值（base_url 需要）
            if 'account' not in args or not args['account']:
                # 使用第一个支持的账号作为占位符（实际不会用于认证）
                args['account'] = HuaweiCommonTools.SUPPORTED_ACCOUNTS[0]
                logger.info(
                    f'使用 Authorization 请求头，设置占位账号: '
                    f'{args["account"]}'
                )
            else:
                logger.info(
                    f'使用 Authorization 请求头，保留参数中的账号: '
                    f'{args["account"]}'
                )
        else:
            # 没有 Authorization，需要验证账号
            account = None

            # 先尝试从 context 中获取账号
            if ctx:
                try:
                    # 从 context.metadata 中查找账号信息
                    metadata = getattr(ctx, 'metadata', {})
                    if metadata and 'account' in metadata:
                        account = metadata['account']
                        logger.info(f'从 context 中提取到账号: {account}')
                except Exception as e:
                    logger.debug(f'从 context 提取账号失败: {e}')

            # 如果 context 中没有，再从参数中提取
            if not account:
                account = _extract_account_from_args(tool_name, args)

            # 如果参数中也没有，尝试从 context 的其他地方查找
            if not account and ctx:
                try:
                    # 尝试从请求参数或查询中提取
                    request_params = getattr(ctx, 'request_params', {})
                    for key, value in request_params.items():
                        if isinstance(value, str):
                            extracted = (
                                HuaweiCommonTools._extract_account(value)
                            )
                            if extracted:
                                account = extracted
                                logger.info(
                                    f'从 context.request_params 中提取到'
                                    f'账号: {account}'
                                )
                                break
                except Exception as e:
                    logger.debug(
                        f'从 context.request_params 提取账号失败: {e}'
                    )

            if not account:
                # 缺少账号，抛出异常要求用户输入
                available_accounts = ", ".join(
                    HuaweiCommonTools.SUPPORTED_ACCOUNTS
                )
                error_msg = (
                    f'工具 "{tool_name}" 需要账号信息。\n\n'
                    f'未检测到账号信息，请选择要使用的账号。\n\n'
                    f'可用账号: {available_accounts}\n\n'
                    f'请在参数中指定账号，或在查询中包含账号名称。'
                )
                logger.warning(f'工具 {tool_name} 缺少账号信息')
                raise UserInputRequiredError(error_msg)

            # 验证账号是否在支持列表中
            if account not in HuaweiCommonTools.SUPPORTED_ACCOUNTS:
                available_accounts = ', '.join(
                    HuaweiCommonTools.SUPPORTED_ACCOUNTS
                )
                error_msg = (
                    f'账号 "{account}" 不在支持列表中。\n\n'
                    f'可用账号: {available_accounts}'
                )
                logger.warning(f'账号 {account} 不在支持列表中')
                raise ValueError(error_msg)

            # 自动补全到参数中
            args['account'] = account
            logger.info(f'账号验证通过并已补全到参数: {account}')

    # 2. 验证服务（仅对需要服务的工具）
    if tool_name in TOOLS_REQUIRE_SERVICE:
        service = None

        # 先尝试从 context 中获取服务
        if ctx:
            try:
                # 从 context.metadata 中查找服务信息
                metadata = getattr(ctx, 'metadata', {})
                if metadata and 'service' in metadata:
                    service = metadata['service']
                    logger.info(f'从 context 中提取到服务: {service}')
            except Exception as e:
                logger.debug(f'从 context 提取服务失败: {e}')

        # 如果 context 中没有，再从参数中提取
        if not service:
            service = _extract_service_from_args(tool_name, args)

        # 如果参数中也没有，尝试从 context 的其他地方查找
        if not service and ctx:
            try:
                # 尝试从请求参数或查询中提取
                request_params = getattr(ctx, 'request_params', {})
                for key, value in request_params.items():
                    if isinstance(value, str):
                        extracted = (
                            HuaweiCommonTools._extract_service(value)
                        )
                        if extracted:
                            service = extracted
                            logger.info(
                                f'从 context.request_params 中提取到'
                                f'服务: {service}'
                            )
                            break
            except Exception as e:
                logger.debug(
                    f'从 context.request_params 提取服务失败: {e}'
                )

        if not service:
            # 缺少服务，抛出异常要求用户输入
            from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import (
                SUPPORTED_SERVICES
            )
            from huawei_cloud_ops_mcp_server.huaweicloud.pricedocs import (
                PRICE_DOCS
            )

            # 根据工具类型确定可用服务列表
            if tool_name == 'query_price':
                available_services = sorted(PRICE_DOCS.keys())
                service_type_desc = '价格查询'
            else:
                available_services = sorted(SUPPORTED_SERVICES)
                service_type_desc = 'API查询'

            service_list = ', '.join(available_services)
            error_msg = (
                f'工具 "{tool_name}" 需要服务信息。\n\n'
                f'未检测到服务类型，请指定要{service_type_desc}的服务。\n\n'
                f'可用服务: {service_list}\n\n'
                f'请在参数中指定服务，或在查询中包含服务名称（如: ecs, vpc, rds）。'
            )
            logger.warning(f'工具 {tool_name} 缺少服务信息')
            raise UserInputRequiredError(error_msg)

        # 自动补全到参数中
        args['service'] = service
        logger.info(f'服务验证通过并已补全到参数: {service}')


def tool_execution_hook(original_func: Callable) -> Callable:
    """工具执行钩子装饰器

    在工具执行前进行参数验证（账号、服务等）

    Args:
        original_func: 原始工具函数

    Returns:
        Callable: 包装后的工具函数
    """
    @functools.wraps(original_func)
    async def wrapper(*args, **kwargs) -> Any:
        # 获取工具名称
        tool_name = original_func.__name__

        if tool_name in (TOOLS_REQUIRE_ACCOUNT | TOOLS_REQUIRE_SERVICE):
            # 提取 context 和其他参数
            ctx = kwargs.get('ctx')
            tool_kwargs = {k: v for k, v in kwargs.items() if k != 'ctx'}

            # 验证参数（传递 context 用于提取信息）
            await validate_tool_params(tool_name, tool_kwargs, ctx)

            # 将补全后的参数更新回 kwargs
            for key, value in tool_kwargs.items():
                if key != 'ctx':
                    kwargs[key] = value

        # 执行原始工具函数
        return await original_func(*args, **kwargs)

    return wrapper


def main(mcp: FastMCP, transport: str):
    logger.info(f'启动 MCP 服务器,传输方式: {transport}')
    load_tools(mcp)
    load_resources(mcp)
    mcp.run(transport=transport)


async def main_async(
    mcp: FastMCP, transport: str, host: str = None, port: int = None
):
    logger.info(f'启动 MCP 服务器(异步模式),传输方式: {transport}')
    if transport == 'http':
        logger.info(f'HTTP 模式,监听地址: {host}:{port}')
    load_tools(mcp)
    load_resources(mcp)
    if transport == 'http':
        await mcp.run_async(transport=transport, host=host, port=port)
    else:
        await mcp.run_async(transport=transport)


if __name__ == '__main__':
    logger.info('华为云运维 MCP 服务器启动')
    mcp = FastMCP(
        name='huawei-cloud-ops-mcp-server'
    )
    asyncio.run(main_async(mcp, MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT))
