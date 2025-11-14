DCS (分布式缓存服务) API 文档:

常用端点:
1. 查询所有实例列表:
- action: 'v2/{project_id}/instances'
- method: GET
- 功能: 查询租户的缓存实例列表，支持按照条件查询
- 路径参数:
  * project_id (必选): 项目ID。获取方法请参见获取项目ID。
- 查询参数 (可选):
  * instance_id (String): 实例ID。可通过DCS控制台进入实例详情界面查看。
  * include_failure (String): 是否返回创建失败的实例数。可选值:
    - true: 返回创建失败的实例数
    - false: 不返回创建失败的实例数
    - 默认值: false
  * include_delete (String): 是否返回已删除的实例数。可选值:
    - true: 返回已删除的实例数
    - false: 不返回已删除的实例数
    - 默认值: false
  * name (String): 实例名称，支持模糊匹配。
  * offset (Integer): 偏移量，表示生成的列表从此偏移量开始显示，例如偏移量为3时，生成的列表从第4条开始。取值范围: 大于等于0。默认值: 0
  * limit (Integer): 每页显示的条目数量。取值范围: 1-1000。默认值: 10
  * status (String): 实例状态。详细状态说明见缓存实例状态说明，常见状态包括:
    - CREATING: 创建中
    - RUNNING: 运行中
    - ERROR: 错误
    - RESTARTING: 重启中
    - FROZEN: 已冻结
    - EXTENDING: 扩容中
    - RESTORING: 恢复中
    - FLUSHING: 清空中
  * name_equal (String): 按照实例名称进行精确匹配查询。
  * tags (String): 根据实例标签键值对进行查询。{key}表示标签键，{value}表示标签值。如果同时使用多个标签键值对进行查询，中间使用逗号分隔开，表示查询同时包含指定标签键值对的实例。
  * ip (String): 连接缓存实例的IP地址，如192.168.7.146。可以通过DCS控制台进入实例详情界面查看。
  * capacity (String): 缓存实例的容量，单位：GB。
  * is_recycle (Boolean): 是否查询回收站的实例。可选值:
    - true: 返回回收站的实例
    - false: 返回缓存实例列表
    - 默认值: false
- 响应格式:
  * instance_num (Integer): 实例个数
  * instances (Array): 实例列表，每个实例对象包含以下主要字段:
    - instance_id (String): 实例ID
    - name (String): 实例名称
    - status (String): 实例状态
    - description (String): 实例描述
    - spec_code (String): 实例规格代码
    - engine (String): 缓存引擎类型，可选值: Redis、Memcached
    - engine_version (String): 缓存引擎版本
    - cpu_type (String): CPU类型
    - capacity (String): 实例容量，单位：GB
    - ip (String): 连接缓存实例的IP地址
    - port (Integer): 连接缓存实例的端口号
    - resource_spec_code (String): 资源规格代码
    - security_group_id (String): 安全组ID
    - security_group_name (String): 安全组名称
    - subnet_id (String): 子网ID
    - subnet_name (String): 子网名称
    - subnet_cidr (String): 子网网段
    - vpc_id (String): 虚拟私有云ID
    - vpc_name (String): 虚拟私有云名称
    - created_at (String): 创建时间，ISO8601格式
    - updated_at (String): 更新时间，ISO8601格式
    - user_id (String): 用户ID
    - user_name (String): 用户名
    - maintain_begin (String): 维护时间窗开始时间，格式为HH:mm:ss
    - maintain_end (String): 维护时间窗结束时间，格式为HH:mm:ss
    - enable_publicip (Boolean): 是否开启公网访问
    - publicip_id (String): 公网IP ID
    - publicip_address (String): 公网IP地址
    - enable_ssl (Boolean): 是否开启SSL
    - service_upgrade (Boolean): 服务升级状态
    - service_task_id (String): 服务任务ID
    - enterprise_project_id (String): 企业项目ID
    - backup_policy (Object): 备份策略，包含:
      * save_days (Integer): 备份保留天数
      * backup_type (String): 备份类型
      * periodical_backup_plan (Object): 周期性备份计划
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
    - product_id (String): 产品ID
    - security_group_name (String): 安全组名称
    - timezone (String): 时区
    - allocated_memory (Integer): 已分配内存，单位：MB
    - capacity_threshold (Integer): 容量阈值
    - user_id (String): 用户ID
    - ipv6_enable (Boolean): 是否启用IPv6
    - ipv6 (String): IPv6地址
    - enable_whitelist (Boolean): 是否启用白名单
    - whitelist (String): 白名单
    - enable_auto_renew (Boolean): 是否自动续费
    - charging_mode (Integer): 计费模式，0表示按需，1表示包年/包月
    - order_id (String): 订单ID
    - period_type (String): 订购周期类型
    - period_num (Integer): 订购周期数
    - expire_time (String): 到期时间，ISO8601格式
    - az_codes (Array): 可用区代码列表
    - access_user (String): 访问用户名
    - domain_name (String): 域名
    - read_endpoints (Array): 只读节点列表
    - write_endpoints (Array): 写节点列表
    - features (Object): 特性信息
    - sub_status (String): 子状态
    - public_domain (String): 公网域名
    - private_domain (String): 私网域名
- 示例:
  * 查询所有实例: GET /v2/{project_id}/instances
  * 按实例ID查询: GET /v2/{project_id}/instances?instance_id={instance_id}
  * 按名称模糊查询: GET /v2/{project_id}/instances?name=test
  * 按名称精确查询: GET /v2/{project_id}/instances?name_equal=test-instance
  * 按状态查询: GET /v2/{project_id}/instances?status=RUNNING
  * 按IP查询: GET /v2/{project_id}/instances?ip=192.168.7.146
  * 按容量查询: GET /v2/{project_id}/instances?capacity=2
  * 分页查询: GET /v2/{project_id}/instances?offset=0&limit=50
  * 标签过滤: GET /v2/{project_id}/instances?tags=key1=value1,key2=value2
  * 包含创建失败的实例: GET /v2/{project_id}/instances?include_failure=true
  * 包含已删除的实例: GET /v2/{project_id}/instances?include_delete=true
  * 查询回收站实例: GET /v2/{project_id}/instances?is_recycle=true
  * 组合查询: GET /v2/{project_id}/instances?status=RUNNING&limit=20&offset=0&name=test

