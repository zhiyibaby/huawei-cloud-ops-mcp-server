"""
工具执行钩子测试

这个测试文件演示了工具执行钩子的功能和使用方法。
"""
import asyncio
import pytest
from unittest.mock import patch

from huawei_cloud_ops_mcp_server.server import (
    _extract_account_from_args,
    _extract_service_from_args,
    _check_authorization,
    validate_tool_params,
    TOOLS_REQUIRE_ACCOUNT,
    TOOLS_REQUIRE_SERVICE
)
from huawei_cloud_ops_mcp_server.tools.common_tools import (
    UserInputRequiredError
)


class TestAccountExtraction:
    """测试账号提取功能"""

    def test_extract_account_from_account_param(self):
        """测试从 account 参数中提取账号"""
        args = {'account': 'xiaohei2018', 'service': 'ecs'}
        result = _extract_account_from_args('huawei_api_request', args)
        assert result == 'xiaohei2018'

    def test_extract_account_from_query_param(self):
        """测试从 query 参数中提取账号"""
        args = {
            'query': '使用 krsk2021 账号查询 ECS 实例',
            'service': 'ecs'
        }
        result = _extract_account_from_args('huawei_api_request', args)
        assert result == 'krsk2021'

    def test_no_account_found(self):
        """测试未找到账号的情况"""
        args = {'service': 'ecs', 'action': 'list'}
        result = _extract_account_from_args('huawei_api_request', args)
        assert result is None


class TestServiceExtraction:
    """测试服务提取功能"""

    def test_extract_service_from_service_param(self):
        """测试从 service 参数中提取服务"""
        args = {'account': 'xiaohei2018', 'service': 'ecs'}
        result = _extract_service_from_args('huawei_api_request', args)
        assert result == 'ecs'

    def test_extract_service_from_query_param(self):
        """测试从 query 参数中提取服务（中文）"""
        args = {
            'account': 'xiaohei2018',
            'query': '查询云服务器价格'
        }
        result = _extract_service_from_args('query_price', args)
        assert result == 'ecs'

    def test_extract_service_from_query_param_english(self):
        """测试从 query 参数中提取服务（英文）"""
        args = {
            'account': 'xiaohei2018',
            'query': '查询 vpc 配置'
        }
        result = _extract_service_from_args('huawei_api_request', args)
        assert result == 'vpc'

    def test_no_service_found(self):
        """测试未找到服务的情况"""
        args = {'account': 'xiaohei2018', 'action': 'list'}
        result = _extract_service_from_args('huawei_api_request', args)
        assert result is None


class TestAuthorizationCheck:
    """测试 Authorization 检查功能"""

    @patch('huawei_cloud_ops_mcp_server.server.get_http_request')
    def test_with_authorization_header(self, mock_get_request):
        """测试有 Authorization 头的情况"""
        mock_request = MagicMock()
        mock_request.headers = {'Authorization': 'Bearer token123'}
        mock_get_request.return_value = mock_request

        result = _check_authorization()
        assert result is True

    @patch('huawei_cloud_ops_mcp_server.server.get_http_request')
    def test_without_authorization_header(self, mock_get_request):
        """测试没有 Authorization 头的情况"""
        mock_request = MagicMock()
        mock_request.headers = {}
        mock_get_request.return_value = mock_request

        result = _check_authorization()
        assert result is False

    @patch('huawei_cloud_ops_mcp_server.server.get_http_request')
    def test_exception_handling(self, mock_get_request):
        """测试异常处理（stdio 模式）"""
        mock_get_request.side_effect = Exception('No HTTP request')

        result = _check_authorization()
        assert result is False


class TestValidateToolParams:
    """测试工具参数验证功能"""

    @pytest.mark.asyncio
    @patch('huawei_cloud_ops_mcp_server.server._check_authorization')
    async def test_validate_with_valid_account(self, mock_check_auth):
        """测试有效账号的验证"""
        mock_check_auth.return_value = False

        args = {
            'account': 'xiaohei2018',
            'service': 'ecs',
            'action': 'list'
        }

        # 应该不抛出异常
        await validate_tool_params('huawei_api_request', args)

    @pytest.mark.asyncio
    @patch('huawei_cloud_ops_mcp_server.server._check_authorization')
    async def test_validate_with_authorization_header(self, mock_check_auth):
        """测试有 Authorization 头时跳过账号验证"""
        mock_check_auth.return_value = True

        args = {
            'service': 'ecs',
            'action': 'list'
        }

        # 应该不抛出异常（因为有 Authorization 头）
        await validate_tool_params('huawei_api_request', args)

    @pytest.mark.asyncio
    @patch('huawei_cloud_ops_mcp_server.server._check_authorization')
    async def test_validate_missing_account(self, mock_check_auth):
        """测试缺少账号时抛出异常"""
        mock_check_auth.return_value = False

        args = {
            'service': 'ecs',
            'action': 'list'
        }

        # 应该抛出 UserInputRequiredError
        with pytest.raises(UserInputRequiredError) as exc_info:
            await validate_tool_params('huawei_api_request', args)

        assert '账号信息' in str(exc_info.value)

    @pytest.mark.asyncio
    @patch('huawei_cloud_ops_mcp_server.server._check_authorization')
    async def test_validate_invalid_account(self, mock_check_auth):
        """测试无效账号时抛出异常"""
        mock_check_auth.return_value = False

        args = {
            'account': 'invalid_account',
            'service': 'ecs',
            'action': 'list'
        }

        # 应该抛出 ValueError
        with pytest.raises(ValueError) as exc_info:
            await validate_tool_params('huawei_api_request', args)

        assert 'invalid_account' in str(exc_info.value)
        assert '不在支持列表中' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_validate_missing_service(self):
        """测试缺少服务时抛出异常"""
        args = {
            'filters': {'region': '华北-北京四'}
        }

        # 应该抛出 UserInputRequiredError
        with pytest.raises(UserInputRequiredError) as exc_info:
            await validate_tool_params('query_price', args)

        assert '服务信息' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_validate_with_valid_service(self):
        """测试有效服务的验证"""
        args = {
            'service': 'ecs',
            'filters': {'region': '华北-北京四'}
        }

        # 应该不抛出异常
        await validate_tool_params('query_price', args)


class TestHookConfiguration:
    """测试钩子配置"""

    def test_tools_require_account(self):
        """测试需要账号验证的工具列表"""
        assert 'huawei_api_request' in TOOLS_REQUIRE_ACCOUNT

    def test_tools_require_service(self):
        """测试需要服务验证的工具列表"""
        assert 'huawei_api_request' in TOOLS_REQUIRE_SERVICE
        assert 'query_price' in TOOLS_REQUIRE_SERVICE


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
