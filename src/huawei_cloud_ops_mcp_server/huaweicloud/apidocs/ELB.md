ELB (弹性负载均衡) API 文档:

常用端点:
1. 查询负载均衡列表:
- action: 'v3/{project_id}/elb/loadbalancers'
- method: GET
- 接口约束:
  * 分页查询使用的参数为marker、limit、page_reverse。
  * marker和page_reverse只有和limit一起使用时才会生效，单独使用无效。
- 路径参数:
  - project_id (必选): 项目ID。长度为32个字符，由小写字母和数字组成。获取方式请参见获取项目ID文档。
- 查询参数 (均为可选):
  - marker: 上一页最后一条记录的ID。必须与limit一起使用。不指定时表示查询第一页。该字段不允许为空或无效的ID。
  - limit: 每页返回的个数。取值范围：0-2000。默认取值：2000。
  - page_reverse: 是否反向查询。必须与limit一起使用。当page_reverse=true时，若要查询上一页，marker取值为当前页返回值的previous_marker。取值范围：true（查询上一页）、false（查询下一页）。默认取值：false。
  - id: 负载均衡器ID。支持多值查询，查询条件格式：id=xxx&id=xxx。
  - name: 负载均衡器名称。支持多值查询，查询条件格式：name=xxx&name=xxx。
  - description: 负载均衡器的描述信息。支持多值查询，查询条件格式：description=xxx&description=xxx。
  - operating_status: 负载均衡器的操作状态。取值范围：ONLINE（在线）、FROZEN（冻结）。支持多值查询。
  - provisioning_status: 负载均衡器的配置状态。取值范围：ACTIVE（该字段为预留字段，暂未启用）。支持多值查询。
  - admin_state_up: 负载均衡器的管理状态。true：启用负载均衡器；false：停用负载均衡器。
  - vip_address: 负载均衡器的内网IP地址。
  - vip_port_id: 负载均衡器内网IP对应的端口ID。
  - vip_subnet_id: 负载均衡器所在的子网ID。
  - vpc_id: 负载均衡器所在的虚拟私有云ID。
  - enterprise_project_id: 企业项目ID。支持多值查询。
  - provider: 负载均衡器的provider名称。支持多值查询。
  - tags: 负载均衡器的标签列表。支持多值查询，查询条件格式：tags=key1=value1&tags=key2=value2。
  - any_tags: 负载均衡器的标签列表，包含任意一个标签。支持多值查询，查询条件格式：any_tags=key1=value1&any_tags=key2=value2。
  - not_tags: 负载均衡器的标签列表，不包含任意一个标签。支持多值查询，查询条件格式：not_tags=key1=value1&not_tags=key2=value2。
  - tags_any: 负载均衡器的标签列表，包含任意一个标签。支持多值查询，查询条件格式：tags_any=key1=value1&tags_any=key2=value2。
  - not_any_tags: 负载均衡器的标签列表，不包含任意一个标签。支持多值查询，查询条件格式：not_any_tags=key1=value1&not_any_tags=key2=value2。
  - created_at: 负载均衡器的创建时间。支持范围查询，查询条件格式：created_at=gt:2023-01-01T00:00:00Z&created_at=lt:2023-12-31T23:59:59Z。
  - updated_at: 负载均衡器的更新时间。支持范围查询，查询条件格式：updated_at=gt:2023-01-01T00:00:00Z&updated_at=lt:2023-12-31T23:59:59Z。
  - guaranteed: 是否独享型负载均衡器。true：独享型；false：共享型。
  - eips: 负载均衡器绑定的公网IP地址。支持多值查询。
  - ipv6_vip_address: 负载均衡器的IPv6内网IP地址。
  - ipv6_vip_virsubnet_id: 负载均衡器所在的IPv6子网ID。
  - ipv6_vip_port_id: 负载均衡器IPv6内网IP对应的端口ID。
  - availability_zone_list: 负载均衡器所在的可用区列表。支持多值查询。
  - l4_flavor_id: 网络型规格ID。
  - l4_scale_flavor_id: 四层弹性规格ID。
  - l7_flavor_id: 应用型规格ID。
  - l7_scale_flavor_id: 七层弹性规格ID。
  - billing_info: 负载均衡器的计费信息。
  - member_address: 后端服务器的IP地址。支持多值查询。
  - member_device_id: 后端服务器对应的弹性云服务器ID。支持多值查询。
  - member_deletion_protection_enable: 是否开启删除保护。true：开启；false：关闭。
  - listener_id: 监听器ID。支持多值查询。
  - listener_protocol: 监听器的前端协议类型。支持多值查询。
  - listener_protocol_port: 监听器的前端协议端口。支持多值查询。
  - publicips: 负载均衡器绑定的公网IP地址。支持多值查询。
  - global_eips: 负载均衡器绑定的全球公网IP地址。支持多值查询。
- 响应结构:
  - loadbalancers: 负载均衡器对象列表
    - id: 负载均衡器ID
    - name: 负载均衡器名称
    - description: 负载均衡器描述
    - operating_status: 操作状态 (ONLINE/FROZEN)
    - provisioning_status: 配置状态 (ACTIVE)
    - admin_state_up: 管理状态 (true/false)
    - vip_address: 内网IP地址
    - vip_port_id: 内网IP对应的端口ID
    - vip_subnet_id: 子网ID
    - vpc_id: 虚拟私有云ID
    - provider: provider名称
    - pools: 后端服务器组列表
    - listeners: 监听器列表
    - tags: 标签列表
    - created_at: 创建时间
    - updated_at: 更新时间
    - enterprise_project_id: 企业项目ID
    - tenant_id: 租户ID
    - project_id: 项目ID
    - ipv6_vip_address: IPv6内网IP地址
    - ipv6_vip_virsubnet_id: IPv6子网ID
    - ipv6_vip_port_id: IPv6内网IP对应的端口ID
    - availability_zone_list: 可用区列表
    - l4_flavor_id: 网络型规格ID
    - l4_scale_flavor_id: 四层弹性规格ID
    - l7_flavor_id: 应用型规格ID
    - l7_scale_flavor_id: 七层弹性规格ID
    - billing_info: 计费信息
    - guaranteed: 是否独享型负载均衡器 (true/false)
    - eips: 绑定的公网IP地址列表
    - publicips: 绑定的公网IP地址列表
    - global_eips: 绑定的全球公网IP地址列表
    - page_info: 分页信息
      - previous_marker: 上一页的marker值
      - current_count: 当前页的记录数
- 使用示例:
  * 查询所有负载均衡器: GET /v3/{project_id}/elb/loadbalancers
  * 按名称查询: GET /v3/{project_id}/elb/loadbalancers?name=my-loadbalancer
  * 按名称多值查询: GET /v3/{project_id}/elb/loadbalancers?name=lb1&name=lb2
  * 按操作状态查询: GET /v3/{project_id}/elb/loadbalancers?operating_status=ONLINE
  * 按VPC ID查询: GET /v3/{project_id}/elb/loadbalancers?vpc_id=vpc-xxxxx
  * 按内网IP查询: GET /v3/{project_id}/elb/loadbalancers?vip_address=192.168.1.100
  * 按子网ID查询: GET /v3/{project_id}/elb/loadbalancers?vip_subnet_id=subnet-xxxxx
  * 分页查询: GET /v3/{project_id}/elb/loadbalancers?marker={loadbalancer_id}&limit=20
  * 反向分页查询: GET /v3/{project_id}/elb/loadbalancers?marker={loadbalancer_id}&limit=20&page_reverse=true
  * 按ID精确查询: GET /v3/{project_id}/elb/loadbalancers?id=lb-xxxxx
  * 按ID多值查询: GET /v3/{project_id}/elb/loadbalancers?id=lb-xxxxx&id=lb-yyyy
  * 按管理状态查询: GET /v3/{project_id}/elb/loadbalancers?admin_state_up=true
  * 组合查询: GET /v3/{project_id}/elb/loadbalancers?vpc_id=vpc-xxxxx&operating_status=ONLINE&admin_state_up=true&limit=50
  * 按企业项目查询: GET /v3/{project_id}/elb/loadbalancers?enterprise_project_id=ep-xxxxx
  * 按标签查询: GET /v3/{project_id}/elb/loadbalancers?tags=key1=value1
  * 按标签多值查询: GET /v3/{project_id}/elb/loadbalancers?tags=key1=value1&tags=key2=value2
  * 按任意标签查询: GET /v3/{project_id}/elb/loadbalancers?any_tags=key1=value1&any_tags=key2=value2
  * 按描述信息查询: GET /v3/{project_id}/elb/loadbalancers?description=production
  * 按创建时间范围查询: GET /v3/{project_id}/elb/loadbalancers?created_at=gt:2023-01-01T00:00:00Z&created_at=lt:2023-12-31T23:59:59Z
  * 按独享型查询: GET /v3/{project_id}/elb/loadbalancers?guaranteed=true
  * 按IPv6地址查询: GET /v3/{project_id}/elb/loadbalancers?ipv6_vip_address=2001:db8::1
  * 按可用区查询: GET /v3/{project_id}/elb/loadbalancers?availability_zone_list=cn-north-1a&availability_zone_list=cn-north-1b
  * 按监听器ID查询: GET /v3/{project_id}/elb/loadbalancers?listener_id=lsr-xxxxx
  * 按监听器协议查询: GET /v3/{project_id}/elb/loadbalancers?listener_protocol=HTTP
  * 按后端服务器IP查询: GET /v3/{project_id}/elb/loadbalancers?member_address=192.168.1.10
  * 按公网IP查询: GET /v3/{project_id}/elb/loadbalancers?eips=1.2.3.4