CSS (云搜索服务) API 文档:

常用端点:
1. 查询云搜索列表:
- action: 'v1.0/{project_id}/clusters'
- method: GET
- 功能: 查询并显示集群列表以及集群的状态，主要包括节点对象列表、Kibana公网访问信息、公网IP信息、集群内网访问IPv4地址和端口号等
- 路径参数:
  * project_id (必选): 项目ID。获取方法请参见获取项目ID和名称。
- 查询参数 (可选):
  * offset (Integer): 指定查询起始值。取值范围：1-1000。默认值为1，即从第1个集群开始查询。
  * limit (Integer): 指定查询不同集群引擎类型的集群总数。取值范围：1-1000。默认值为10，即一次查询10个集群信息。
  * datastoreType (String): 集群引擎类型。可选值:
    - elasticsearch: 基于开源Elasticsearch提供在线分布式搜索、日志统计报表、语义搜索等功能
    - logstash: 基于开源Logstash提供数据收集、转换、清洗、解析等功能
    - opensearch: 基于开源OpenSearch提供分布式搜索、日志统计报表、语义搜索等功能，是CSS服务Elasticsearch集群的下一代版本
    参数为空时查询列表显示所有集群类型。默认值为空。
- 请求Header参数:
  * X-Auth-Token (必选, string): 从IAM服务获取的用户Token。请参考认证鉴权。
- 响应格式:
  * totalSize (Integer): 集群个数。若指定了datastoreType值，显示指定类型集群个数，反之为所有集群个数。
  * clusters (Array): 集群对象列表，每个集群对象包含以下主要字段:
    - datastore (Object): 集群类型和版本信息，包含:
      * type (String): 集群引擎类型，可选值: elasticsearch、logstash、opensearch
      * version (String): 集群版本号
    - snapshotPolicy (Object): 集群自动快照策略相关信息，包含:
      * bucket (String): 快照存储的OBS桶名称
      * basePath (String): 快照在OBS桶中的存放路径
      * agency (String): 委托名称
      * keepday (Integer): 快照保留天数
      * period (String): 快照创建周期
      * prefix (String): 快照命名前缀
      * schedule (Object): 快照创建时间
      * enable (Boolean): 是否启用自动快照
    - instances (Array): 集群节点对象列表，每个节点包含:
      * id (String): 节点ID
      * name (String): 节点名称
      * type (String): 节点类型
      * azCode (String): 可用区编码
      * status (String): 节点状态
      * spec (Object): 节点规格信息
      * volume (Object): 节点存储信息
      * resourceId (String): 资源ID
      * ip (String): 节点IP地址
      * port (Integer): 节点端口号
    - publicKibanaResp (Object): 公网访问信息，包括IP地址、白名单、宽带信息等，包含:
      * publicKibanaIp (String): Kibana公网IP地址（Elasticsearch集群）或Dashboards公网IP地址（OpenSearch集群）
      * publicKibanaPort (Integer): Kibana公网访问端口（Elasticsearch集群）或Dashboards公网访问端口（OpenSearch集群）
      * elbAddress (String): 负载均衡器地址
      * bandwidthSize (Integer): 公网带宽大小，单位为Mbit/s
      * publicKibanaWhitelist (String): 公网访问白名单
    - elbWhiteList (Object): 公网访问控制信息，包含:
      * enableWhiteList (Boolean): 是否启用白名单
      * whiteList (String): 白名单IP地址列表
    - updated (String): 更新时间，ISO8601格式，例如: 2020-01-20T07:43:01.977Z
    - name (String): 集群名称
    - created (String): 创建时间，ISO8601格式，例如: 2020-01-20T07:43:01.977Z
    - id (String): 集群ID
    - status (String): 集群状态，可选值:
      - 100: 创建中
      - 200: 可用
      - 300: 不可用
      - 303: 创建失败
      - 800: 冻结
    - endpoint (String): 集群访问地址
    - vpcId (String): 虚拟私有云ID
    - subnetId (String): 子网ID
    - securityGroupId (String): 安全组ID
    - vpcepIp (String): 终端节点IP地址
    - bandwidthSize (Integer): 公网带宽大小，单位为Mbit/s
    - httpsEnable (Boolean): 是否启用HTTPS
    - authorityEnable (Boolean): 是否启用安全认证
    - diskEncrypted (Boolean): 是否启用磁盘加密
    - backupAvailable (Boolean): 是否支持备份
    - actionProgress (Object): 集群操作进度信息
    - actions (Array): 集群可执行的操作列表
    - enterpriseProjectId (String): 企业项目ID
    - tags (Array): 标签列表
    - payInfo (Object): 计费信息
    - period (Boolean): 是否为包周期集群
    - datacenter (String): 数据中心
    - isPeriod (String): 是否包周期
    - publicIp (String): 公网IP地址
    - traffic (String): 流量
    - publicKibanaIp (String): Kibana公网IP（Elasticsearch集群）或Dashboards公网IP（OpenSearch集群）
    - publicKibanaPort (Integer): Kibana公网端口（Elasticsearch集群）或Dashboards公网端口（OpenSearch集群）
    - publicKibanaWhitelist (String): 公网访问白名单
    - publicAccess (String): 公网访问状态
    - elbWhiteList (Object): 公网访问白名单配置
    - failedReasons (Object): 失败原因（如果存在）
- 示例:
  * 查询所有集群: GET /v1.0/{project_id}/clusters
  * 分页查询: GET /v1.0/{project_id}/clusters?offset=1&limit=20
  * 按引擎类型查询: GET /v1.0/{project_id}/clusters?datastoreType=elasticsearch
  * 组合查询: GET /v1.0/{project_id}/clusters?datastoreType=opensearch&offset=1&limit=50

