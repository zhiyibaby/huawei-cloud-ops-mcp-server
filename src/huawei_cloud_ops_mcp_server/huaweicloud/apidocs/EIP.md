EIP (弹性公网IP) API 文档:

常用端点:
1. 查询弹性公网IP列表:
- action: 'v3/{project_id}/eip/publicips'
- method: GET
- 功能: 查询用户当前局点全量弹性公网IP列表信息
- 路径参数:
  * project_id (必选): 项目ID，获取项目ID请参见获取项目ID 最大长度：32
- 查询参数 (可选):
  * marker (String): 分页查询起始的资源ID，为空时为查询第一页 最小长度：0 最大长度：36
  * offset (Integer): 分页查询起始的资源序号 最小值：0 最大值：99999
  * limit (Integer): 每页返回的资源个数 取值范围：1~2000 最小值：0 最大值：2000
  * fields (Array of strings): 查询字段，形式为"fields=id&fields=owner&..." 支持字段：id/project_id/ip_version/type/public_ip_address/public_ipv6_address/network_type/status/description/created_at/updated_at/vnic/bandwidth/associate_instance_type/associate_instance_id/lock_status/billing_info/tags/enterprise_project_id/allow_share_bandwidth_types/public_border_group/alias/publicip_pool_name/publicip_pool_id 数组长度：0 - 99
  * id (Array of strings): 根据id查询，支持查询多个id 数组长度：0 - 100
  * public_ip_address (Array of strings): 根据公网IP地址查询，支持查询多个地址 数组长度：0 - 100
  * public_ipv6_address (Array of strings): 根据公网IPv6地址查询，支持查询多个地址 数组长度：0 - 100
  * ip_version (Integer): 根据IP版本查询，可选值：4（IPv4）、6（IPv6）
  * type (String): 根据类型查询，可选值：5_bgp（全动态BGP）、5_sbgp（静态BGP）、5_telcom（中国电信）、5_union（中国联通）、5_lvwang（中国移动）
  * network_type (String): 根据网络类型查询，可选值：5_bgp（全动态BGP）、5_sbgp（静态BGP）、5_telcom（中国电信）、5_union（中国联通）、5_lvwang（中国移动）
  * status (String): 根据状态查询，可选值：
    - FREEZED: 冻结
    - BIND_ERROR: 绑定失败
    - BINDING: 绑定中
    - PENDING_CREATE: 创建中
    - PENDING_DELETE: 删除中
    - PENDING_UPDATE: 更新中
    - DOWN: 未绑定
    - ACTIVE: 正常
    - ELB: 绑定ELB
    - ERROR: 错误
  * alias (String): 根据别名查询，支持模糊匹配
  * vnic.private_ip_address (String): 根据私网IP地址查询
  * vnic.vpc_id (String): 根据VPC ID查询
  * vnic.port_id (String): 根据端口ID查询
  * vnic.device_id (String): 根据设备ID查询
  * vnic.device_owner (String): 根据设备所有者查询
  * vnic.instance_id (String): 根据实例ID查询
  * vnic.instance_type (String): 根据实例类型查询
  * bandwidth.id (Array of strings): 根据带宽ID查询，支持查询多个ID 数组长度：0 - 100
  * bandwidth.name (Array of strings): 根据带宽名称查询，支持查询多个名称 数组长度：0 - 100
  * bandwidth.size (Array of integers): 根据带宽大小查询，支持查询多个大小 数组长度：0 - 100
  * bandwidth.share_type (String): 根据带宽共享类型查询，可选值：PER（独享）、WHOLE（共享）
  * bandwidth.charge_mode (String): 根据带宽计费模式查询，可选值：traffic（按流量计费）、bandwidth（按带宽计费）
  * associate_instance_type (String): 根据关联实例类型查询，可选值：PORT、NATGW、ELB、VPN、ELBV1
  * associate_instance_id (Array of strings): 根据关联实例ID查询，支持查询多个ID 数组长度：0 - 100
  * enterprise_project_id (Array of strings): 根据企业项目ID查询，支持查询多个ID 数组长度：0 - 100
  * tags (String): 根据标签查询，格式为 key=value。支持多标签查询，多个标签之间是"与"的关系
  * public_border_group (String): 根据公网IP池名称查询
  * charge_mode (String): 根据计费模式查询，可选值：prePaid（包年/包月）、postPaid（按需）
  * billing_info (String): 根据计费信息查询
  * lock_status (String): 根据锁定状态查询，可选值：POLICE（公安冻结）、LOCKED（普通冻结），普通冻结细分状态：ARREAR（欠费）、DELABLE（可删除）
  * freezed_status (String): 根据冻结状态查询
  * sort_key (String): 排序字段，可选值：id、public_ip_address、public_ipv6_address、ip_version、created_at、updated_at
  * sort_dir (String): 排序方向，可选值：asc（升序）、desc（降序）
- 响应格式:
  * publicips (Array): 弹性公网IP列表，每个EIP对象包含以下主要字段:
    - id (String): 弹性公网IP的ID，格式为UUID
    - project_id (String): 项目ID
    - ip_version (Integer): IP版本，4表示IPv4，6表示IPv6
    - type (String): 弹性公网IP的类型
    - public_ip_address (String): 弹性公网IP的IPv4地址
    - public_ipv6_address (String): 弹性公网IP的IPv6地址（如果存在）
    - network_type (String): 网络类型
    - status (String): 弹性公网IP的状态
    - description (String): 弹性公网IP的描述信息
    - created_at (String): 创建时间，ISO8601格式，例如: 2022-03-17T09:46:22Z
    - updated_at (String): 更新时间，ISO8601格式，例如: 2022-03-30T02:46:04Z
    - vnic (Object): 虚拟网卡信息，包含:
      * private_ip_address (String): 私网IP地址
      * device_id (String): 设备ID
      * device_owner (String): 设备所有者
      * vpc_id (String): VPC ID
      * port_id (String): 端口ID
      * mac (String): MAC地址
      * vtep (String): VTEP地址
      * vni (Integer): VNI
      * instance_id (String): 实例ID
      * instance_type (String): 实例类型
      * port_profile (String): 端口配置文件
      * port_vif_details (String): 端口VIF详情
    - bandwidth (Object): 带宽信息，包含:
      * id (String): 带宽ID
      * size (Integer): 带宽大小（Mbit/s）
      * share_type (String): 共享类型，PER表示独享，WHOLE表示共享
      * charge_mode (String): 计费模式，traffic表示按流量计费，bandwidth表示按带宽计费
      * name (String): 带宽名称
      * billing_info (String): 计费信息
    - associate_instance_type (String): 关联实例类型，可选值：PORT、NATGW、ELB、VPN、ELBV1
    - associate_instance_id (String): 关联实例ID
    - lock_status (String): 锁定状态，POLICE表示公安冻结，LOCKED表示普通冻结
    - freezed_status (String): 冻结状态
    - allow_share_bandwidth_types (Array): 允许共享的带宽类型列表
    - publicip_pool_id (String): 公网IP池ID
    - publicip_pool_name (String): 公网IP池名称
    - public_border_group (String): 公网IP池组
    - alias (String): 弹性公网IP的别名
    - enterprise_project_id (String): 企业项目ID
    - billing_info (String): 计费信息
    - tags (Array): 标签列表，格式为 "key=value"
  * page_info (Object): 分页信息，包含:
    * previous_marker (String): 翻页时，作为前一页的marker取值 最小长度：0 最大长度：36
    * next_marker (String): 翻页时，作为后一页的marker取值 最小长度：0 最大长度：36
    * current_count (Integer): 当前页的数据总数 最小值：0 最大值：99999
  * total_count (Integer): 总记录数
  * request_id (String): 请求ID
- 示例:
  * 查询所有EIP: GET /v3/{project_id}/eip/publicips
  * 按公网IP地址查询: GET /v3/{project_id}/eip/publicips?public_ip_address=88.88.1.141
  * 按状态查询: GET /v3/{project_id}/eip/publicips?status=ACTIVE
  * 按IP版本查询: GET /v3/{project_id}/eip/publicips?ip_version=4
  * 分页查询: GET /v3/{project_id}/eip/publicips?marker={eip_id}&limit=50
  * 标签过滤: GET /v3/{project_id}/eip/publicips?tags=key=value
  * 按带宽ID查询: GET /v3/{project_id}/eip/publicips?bandwidth.id={bandwidth_id}
  * 按关联实例类型查询: GET /v3/{project_id}/eip/publicips?associate_instance_type=PORT
  * 组合查询: GET /v3/{project_id}/eip/publicips?status=ACTIVE&ip_version=4&limit=20&sort_key=created_at&sort_dir=desc
  * 指定返回字段: GET /v3/{project_id}/eip/publicips?fields=id&fields=public_ip_address&fields=status&fields=bandwidth