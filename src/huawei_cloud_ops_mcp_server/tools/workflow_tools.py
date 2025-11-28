from huawei_cloud_ops_mcp_server.utils import ToolMetadata
from huawei_cloud_ops_mcp_server.logger import logger
from huawei_cloud_ops_mcp_server.huaweicloud.static import (
    prompt_understanding_docs
)


class HuaweiWorkflowTools:
    tool_metadatas = {
        'workflow_guide': ToolMetadata(
            priority=0,  # 最高优先级
            category='workflow',
            timeout=10,
            retryable=False
        ),
        'get_workflow_docs': ToolMetadata(
            priority=1,
            category='documentation',
            timeout=10,
            retryable=False
        ),
    }

    # 价格相关关键词（按长度降序排列，优先匹配更长的组合词）
    PRICE_KEYWORDS = [
        # 组合词（优先匹配）
        '查询价格', '价格查询', '获取价格', '价格信息', '价格表', '价格详情',
        '规格价格', '实例价格', '云服务器价格', 'ECS价格', 'RDS价格',
        'EVS价格', '云硬盘价格', '负载均衡价格', 'ELB价格', '价格计算',
        '价格对比', '价格比较', '查看价格', '了解价格', '价格是多少',
        '多少钱', '多贵', '费用查询', '查询费用', '成本查询', '查询成本',
        '计费查询', '查询计费', '定价查询', '查询定价',
        # 单个词
        '价格', '费用', '成本', '计费', '定价', 'price', 'cost', 'billing',
        'pricing', 'charge', 'charges', 'fee', 'fees'
    ]

    # API相关关键词（排除与价格查询相关的通用词，避免误判）
    # 注意：不包含单独的"查询"、"获取"等词，因为这些词在价格查询中也会出现
    API_KEYWORDS = [
        # 组合词（优先匹配）
        'api接口', '调用api', 'api调用', '接口调用', 'api请求', '接口请求',
        '查询实例', '获取实例', '实例列表', '实例详情', '创建实例', '删除实例',
        '更新实例', '修改实例', '查询服务器', '获取服务器', '服务器列表',
        '查询资源', '获取资源', '资源列表', '资源详情', '监控数据', '查看监控',
        '查询指标', '获取指标', '指标数据', '告警信息', '查询告警',
        '管理资源', '操作资源', '资源操作', '资源管理',
        # 服务相关（这些词通常不会单独出现在价格查询中）
        'api', '接口', '调用', '请求', '操作', '管理', '监控',
        '实例', '服务器', '云服务器', 'ECS', 'VPC', 'RDS', 'EVS', 'ELB',
        '负载均衡', '云硬盘', '数据库', '网络', '镜像',
        'metric', '指标', '告警', '资源',
        # 操作动词（仅在明确的操作场景中使用）
        '创建', '删除', '更新', '修改', '列表', '详情'
    ]

    @staticmethod
    def _is_price_related(query: str) -> bool:
        """判断查询是否与价格相关

        优先匹配更长的组合词，避免误判。
        例如："查询价格"应该被识别为价格查询，而不是API查询。
        """
        query_lower = query.lower()
        # 按长度降序排列，优先匹配更长的组合词
        sorted_keywords = sorted(
            HuaweiWorkflowTools.PRICE_KEYWORDS,
            key=len,
            reverse=True
        )
        for keyword in sorted_keywords:
            if keyword.lower() in query_lower:
                return True
        return False

    @staticmethod
    def _is_api_related(query: str) -> bool:
        """判断查询是否与API相关

        如果查询已经包含价格相关关键词，则不判断为API相关，避免误判。
        例如："查询价格"不应该被识别为API查询。
        """
        query_lower = query.lower()

        # 如果查询包含价格相关关键词，则不判断为API相关
        if HuaweiWorkflowTools._is_price_related(query):
            return False

        # 按长度降序排列，优先匹配更长的组合词
        sorted_keywords = sorted(
            HuaweiWorkflowTools.API_KEYWORDS,
            key=len,
            reverse=True
        )
        for keyword in sorted_keywords:
            if keyword.lower() in query_lower:
                return True
        return False

    @staticmethod
    async def workflow_guide(query: str) -> str:
        """工作流指导工具 - 根据用户查询提供工具调用建议

        此工具具有最高优先级，用于分析用户请求并指导后续工具调用流程。
        工具会先查看理解文档，然后基于文档内容提供准确的工具调用建议。

        Args:
            query: 用户的查询内容或需求描述

        Returns:
            str: 工作流指导建议，包含基于理解文档的详细调用步骤

        工作流规则:
        1. 先查看 prompt_understanding 工具理解文档
        2. 根据文档中的工具列表和调用流程提供建议
        3. 如果查询与价格相关，建议按顺序:
           a. 先查看价格文档 (get_price_structure_doc)
           b. 再调用价格工具 (query_price)
        4. 如果查询与API相关,建议按顺序:
           a. 先查看文档 (get_huawei_api_docs)
           b. 再调用API (huawei_api_request)
        5. 如果同时涉及价格和API,优先处理价格查询

        示例:
            # 价格查询
            workflow_guide("查询ECS云服务器的价格")
            # 返回: 基于理解文档的建议，先调用 get_price_structure_doc,再调用 query_price

            # API查询
            workflow_guide("查询所有ECS实例")
            # 返回: 基于理解文档的建议，先调用 get_huawei_api_docs, 再调用API
        """
        logger.info(f'工作流指导: 分析查询 "{query}"')

        # 先查看理解文档（已加载到 prompt_understanding_docs）
        logger.debug('基于工具理解文档提供指导...')

        # 从文档中提取关键信息
        # 提取支持的服务列表
        supported_services = ['ecs', 'vpc', 'rds', 'evs', 'elb', 'ims', 'ces']

        # 分析查询类型
        is_price = HuaweiWorkflowTools._is_price_related(query)
        is_api = HuaweiWorkflowTools._is_api_related(query)

        service_name = None
        query_lower = query.lower()
        for service in supported_services:
            if service in query_lower or service.upper() in query:
                service_name = service
                break

        # 先查看理解文档（已加载到 prompt_understanding_docs）
        # 基于文档内容提供简化的指导建议

        guidance = []
        guidance.append('=' * 60)
        guidance.append('工作流指导')
        guidance.append('=' * 60)

        # 根据查询类型提供具体建议
        if is_price and is_api:
            guidance.append('检测: 价格+API查询')
            guidance.append('')
            if service_name:
                msg1 = f'1. get_price_structure_doc(service="{service_name}")'
                guidance.append(msg1)
                msg2 = (f'2. query_price(service="{service_name}", '
                        'filters={})')
                guidance.append(msg2)
                msg3 = f'3. get_huawei_api_docs(service="{service_name}")'
                guidance.append(msg3)
                msg4 = f'4. huawei_api_request(service="{service_name}", ...)'
                guidance.append(msg4)
            else:
                guidance.append('1. get_price_structure_doc(service="服务名称")')
                guidance.append('2. query_price(service="服务名称", filters={})')
                guidance.append('3. get_huawei_api_docs(service="服务名称")')
                guidance.append('4. huawei_api_request(service="服务名称", ...)')

        elif is_price:
            guidance.append('检测: 价格查询')
            guidance.append('')
            if service_name:
                msg1 = f'1. get_price_structure_doc(service="{service_name}")'
                guidance.append(msg1)
                msg2 = (f'2. query_price(service="{service_name}", '
                        'filters={})')
                guidance.append(msg2)
            else:
                guidance.append('1. get_price_structure_doc(service="服务名称")')
                guidance.append('2. query_price(service="服务名称", filters={})')

        elif is_api:
            guidance.append('检测: API查询')
            guidance.append('')
            if service_name:
                msg1 = f'1. get_huawei_api_docs(service="{service_name}")'
                guidance.append(msg1)
                msg2 = f'2. huawei_api_request(service="{service_name}", ...)'
                guidance.append(msg2)
            else:
                guidance.append('1. get_huawei_api_docs(service="服务名称")')
                guidance.append('2. huawei_api_request(service="服务名称", ...)')

        else:
            guidance.append('检测: 无法判断类型')
            guidance.append('')
            guidance.append('价格查询: get_price_structure_doc → query_price')
            guidance.append('API操作: get_huawei_api_docs → huawei_api_request')

        guidance.append('')
        guidance.append('提示: 调用 prompt_understanding() 获取完整文档')
        guidance.append('=' * 60)

        doc = '\n'.join(guidance)
        log_msg = (f'工作流指导完成: 查询类型 - 价格={is_price}, '
                   f'API={is_api}, 服务={service_name}')
        logger.info(log_msg)
        return doc

    @staticmethod
    async def prompt_understanding() -> str:
        """获取工具调用理解文档

        返回完整的工具调用规范和工作流程说明文档。

        Returns:
            str: 工具调用理解文档内容
        """
        logger.debug('调用工具: prompt_understanding')
        return prompt_understanding_docs
