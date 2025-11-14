RDS (关系型数据库) API 文档:

常用端点:
1. 查询RDS实例列表:
- action: 'v3/{project_id}/instances'
- method: GET
- 功能: 根据指定条件查询实例列表
- 路径参数:
  * project_id (必选): 租户在某一Region下的项目ID。获取方法请参见获取项目ID文档
- 查询参数 (可选):
  * id (String): 实例ID。"*"为系统保留字符，如果id是以"*"起始，表示按照*后面的值模糊匹配，否则，按照id精确匹配查询。不能只传入"*"
  * name (String): 实例名称。"*"为系统保留字符，如果name是以"*"起始，表示按照*后面的值模糊匹配，否则，按照name精确匹配查询。不能只传入"*"
  * type (String): 实例类型。可选值:
    - Single: 单机实例
    - Ha: 主备实例
    - Replica: 只读实例
    - Enterprise: 分布式实例（企业版）
  * datastore_type (String): 数据库类型。区分大小写。可选值:
    - MySQL
    - PostgreSQL
    - SQLServer
  * vpc_id (String): 虚拟私有云ID，获取方法如下：
    - 方法1：登录虚拟私有云服务的控制台界面，在虚拟私有云的详情页面查找VPC ID
    - 方法2：通过虚拟私有云服务的API接口查询，具体操作可参考查询VPC列表文档
  * subnet_id (String): 子网的网络ID信息，获取方法如下：
    - 方法1：登录虚拟私有云服务的控制台界面，单击VPC下的子网，进入子网详情页面，查找网络ID
    - 方法2：通过虚拟私有云服务的API接口查询，具体操作可参考查询子网列表文档
  * offset (Integer): 索引位置，偏移量。从第一条数据偏移offset条数据后开始查询。必须为数字，不能为负数。取值范围：大于等于0的整数。默认取值：0
  * limit (Integer): 每页记录数。取值范围：1-500。默认取值：100
  * tags (String): 标签过滤，格式为 key=value。支持多标签查询，多个标签之间是"与"的关系
- 响应格式:
  * instances (Array): 实例列表，每个实例对象包含以下主要字段:
    - id (String): 实例ID
    - status (String): 实例状态
    - name (String): 实例名称
    - port (Integer): 数据库端口号
    - type (String): 实例类型
    - ha (Object): 主备实例信息，包含:
      * replication_mode (String): 复制模式
    - region (String): 区域
    - datastore (Object): 数据库信息，包含:
      * type (String): 数据库类型
      * version (String): 数据库版本
    - created (String): 创建时间，ISO8601格式
    - updated (String): 更新时间，ISO8601格式
    - volume (Object): 存储信息，包含:
      * type (String): 存储类型
      * size (Integer): 存储大小，单位为GB
    - nodes (Array): 节点列表，每个节点包含:
      * id (String): 节点ID
      * name (String): 节点名称
      * role (String): 节点角色，如 master、slave
      * status (String): 节点状态
      * availability_zone (String): 可用区
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
    - alias (String): 实例别名
    - private_ips (Array): 内网IP地址列表
    - private_dns_names (Array): 内网域名列表
    - public_dns_names (Array): 公网域名列表
    - public_ips (Array): 公网IP地址列表
    - enable_ssl (Boolean): 是否启用SSL
    - db_user_name (String): 数据库用户名
    - vpc_id (String): 虚拟私有云ID
    - subnet_id (String): 子网ID
    - security_group_id (String): 安全组ID
    - flavor_ref (String): 规格ID
    - switch_strategy (String): 切换策略
    - read_only_by_user (Boolean): 是否只读
    - charge_info (Object): 计费信息，包含:
      * charge_mode (String): 计费模式，如 postPaid（按需）、prePaid（包年/包月）
    - backup_strategy (Object): 备份策略，包含:
      * start_time (String): 备份开始时间
      * keep_days (Integer): 保留天数
    - maintenance_window (String): 维护时间窗口
    - related_instance (Array): 关联实例列表
    - disk_encryption_id (String): 磁盘加密ID
    - enterprise_project_id (String): 企业项目ID
    - time_zone (String): 时区
    - order_id (String): 订单ID
    - associated_with_ddm (Boolean): 是否关联DDM
    - serverless_info (Object): Serverless信息（仅Serverless型实例），包含:
      * max_compute_unit (String): 最大计算单元
      * min_compute_unit (String): 最小计算单元
  * total_count (Integer): 实例总数
- 示例:
  * 查询所有实例: GET /v3/{project_id}/instances
  * 按ID精确查询: GET /v3/{project_id}/instances?id=xxx
  * 按ID模糊查询: GET /v3/{project_id}/instances?id=*xxx
  * 按名称精确查询: GET /v3/{project_id}/instances?name=my-rds
  * 按名称模糊查询: GET /v3/{project_id}/instances?name=*rds
  * 按实例类型查询: GET /v3/{project_id}/instances?type=Ha
  * 按数据库类型查询: GET /v3/{project_id}/instances?datastore_type=MySQL
  * 按VPC ID查询: GET /v3/{project_id}/instances?vpc_id=vpc-xxxxx
  * 按子网ID查询: GET /v3/{project_id}/instances?subnet_id=subnet-xxxxx
  * 分页查询: GET /v3/{project_id}/instances?offset=10&limit=50
  * 按标签查询: GET /v3/{project_id}/instances?tags=key1=value1
  * 组合查询: GET /v3/{project_id}/instances?type=Ha&datastore_type=MySQL&limit=20&offset=0