DDS (文档数据库服务) API 文档:

常用端点:
1. 查询实例列表和详情:
- action: 'v3/{project_id}/instances'
- method: GET
- 功能: 根据指定条件查询实例列表和详情
- 路径参数:
  * project_id (必选): 租户在某一Region下的项目ID。请参考获取项目ID章节获取项目编号。
- 查询参数 (可选):
  * id (String): 实例ID，可以调用"查询实例列表和详情"接口获取。如果未申请实例，可以调用"创建实例"接口创建。
  * name (String): 实例名称。如果name以"*"起始，表示按照"*"后面的值模糊匹配，否则，按照实际填写的name精确匹配查询。
    说明: "*"为系统保留字符，不能只传入该字符。
  * mode (String): 实例类型。可选值:
    - Sharding: 集群实例
    - ReplicaSet: 副本集实例
    - Single: 单节点实例
  * datastore_type (String): 数据库版本类型。取值为"DDS-Community"。
  * vpc_id (String): 虚拟私有云ID，获取方法如下:
    - 方法1: 登录虚拟私有云服务的控制台界面，在虚拟私有云的详情页面查找VPC ID
    - 方法2: 通过虚拟私有云服务的API接口查询，具体操作可参考查询VPC列表
  * subnet_id (String): 子网的网络ID，获取方法如下:
    - 方法1: 登录虚拟私有云服务的控制台界面，单击VPC下的子网，进入子网详情页面，查找网络ID
    - 方法2: 通过虚拟私有云服务的API接口查询，具体操作可参考查询子网列表
  * offset (Integer): 索引位置偏移量，表示从指定project ID下最新的实例创建时间开始，按时间的先后顺序偏移offset条数据后查询对应的实例信息。
    取值大于或等于0。不传该参数时，查询偏移量默认为0，表示从最新的实例创建时间对应的实例开始查询。
  * limit (Integer): 查询实例个数上限值。取值范围：1~100。不传该参数时，默认查询前100条实例信息。
  * tags (String): 根据实例标签键值对进行查询。{key}表示标签键，{value}表示标签值，最多包含20组。key不可以为空或重复，value可以为空。
    如果同时使用多个标签键值对进行查询，中间使用逗号分隔开，表示查询同时包含指定标签键值对的实例。
- 请求Header参数:
  * X-Auth-Token (必选, string): 从IAM服务获取的用户Token。请参考认证鉴权。
- 响应格式:
  * instances (Array): 实例信息列表，每个实例对象包含以下主要字段:
    - id (String): 实例ID
    - name (String): 实例名称
    - status (String): 实例状态，可选值:
      - creating: 创建中
      - normal: 正常
      - abnormal: 异常
      - createfail: 创建失败
      - enlarging: 扩容中
      - reducing: 缩容中
      - switching: 主备切换中
      - frozen: 已冻结
      - data_disk_full: 数据盘满
      - backuping: 备份中
      - restoring: 恢复中
      - restarting: 重启中
    - datastore (Object): 数据库信息，包含:
      * type (String): 数据库类型，取值为"DDS-Community"
      * version (String): 数据库版本号
    - mode (String): 实例类型，可选值: Sharding（集群实例）、ReplicaSet（副本集实例）、Single（单节点实例）
    - region (String): 区域ID
    - availability_zone (String): 可用区ID
    - vpc_id (String): 虚拟私有云ID
    - subnet_id (String): 子网的网络ID
    - security_group_id (String): 安全组ID
    - port (Integer): 数据库端口号
    - ssl (Integer): SSL连接开关，0表示关闭，1表示打开
    - backup_strategy (Object): 备份策略，包含:
      * start_time (String): 备份时间段，格式为"HH:mm-HH:mm"
      * keep_days (Integer): 备份保留天数
    - created (String): 创建时间，ISO8601格式，例如: 2020-01-20T07:43:01.977Z
    - updated (String): 更新时间，ISO8601格式，例如: 2020-01-20T07:43:01.977Z
    - db_user_name (String): 数据库用户名
    - storage_engine (String): 存储引擎，可选值: WiredTiger、RocksDB
    - pay_mode (String): 计费模式，可选值: 0（按需）、1（包年/包月）
    - disk_encryption_id (String): 磁盘加密ID
    - enterprise_project_id (String): 企业项目ID
    - time_zone (String): 时区
    - actions (Array): 实例可执行的操作列表，可选值:
      - CREATE: 创建
      - RESTART: 重启
      - DELETE: 删除
      - MODIFY: 修改
      - GROW: 扩容
      - SWITCHOVER: 主备切换
      - MODIFY_PASSWORD: 修改密码
      - BACKUP: 备份
      - RESTORE: 恢复
    - groups (Array): 实例组信息（仅集群实例有此字段），包含:
      * type (String): 节点类型，可选值: mongos、shard、config
      * volume (Object): 存储信息（仅shard和config节点有此字段），包含:
        - size (String): 存储大小，单位为GB
        - used (String): 已使用存储大小，单位为GB
      * nodes (Array): 节点列表，每个节点包含:
        - id (String): 节点ID
        - name (String): 节点名称
        - status (String): 节点状态
        - role (String): 节点角色，可选值: Primary（主节点）、Secondary（备节点）、Hidden（隐藏节点）
        - private_ip (String): 私网IP地址
        - public_ip (String): 公网IP地址（如果存在）
        - spec_code (String): 规格码
        - availability_zone (String): 可用区
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
  * total_count (Integer): 总记录数
  * request_id (String): 请求ID
- 示例:
  * 查询所有实例: GET /v3/{project_id}/instances
  * 按实例ID查询: GET /v3/{project_id}/instances?id={instance_id}
  * 按名称精确查询: GET /v3/{project_id}/instances?name=test-instance
  * 按名称模糊查询: GET /v3/{project_id}/instances?name=*test
  * 按实例类型查询: GET /v3/{project_id}/instances?mode=ReplicaSet
  * 按VPC查询: GET /v3/{project_id}/instances?vpc_id={vpc_id}
  * 分页查询: GET /v3/{project_id}/instances?offset=0&limit=50
  * 标签过滤: GET /v3/{project_id}/instances?tags=key1=value1,key2=value2
  * 组合查询: GET /v3/{project_id}/instances?mode=ReplicaSet&limit=20&offset=0

