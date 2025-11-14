EVS (云硬盘) API 文档:

常用端点:
1. 查询云硬盘列表:
- action: 'v2/{project_id}/cloudvolumes/detail'
- method: GET
- 功能: 查询所有云硬盘的详细信息
- 路径参数:
  * project_id (必选): 项目ID。获取方法请参见获取项目ID文档
- 查询参数 (可选):
  * marker (String): 通过云硬盘ID进行分页查询，默认为查询第一页数据。marker={{id}}表示查询该云硬盘id后的所有云硬盘的信息(查询结果不包含该id的云硬盘信息)
  * name (String): 云硬盘名称
  * limit (Integer): 返回结果个数限制。默认取值: 1000
  * sort_key (String): 返回结果按该关键字排序。可选值:
    - id: 云硬盘ID
    - status: 云硬盘状态
    - size: 云硬盘大小，单位为GiB
    - created_at: 云硬盘创建时间
    默认取值: created_at
  * offset (Integer): 偏移量。查询云硬盘列表时使用，与limit配合使用。假如共有30个云硬盘，设置offset为11，limit为10，即为从第12个云硬盘开始查询，一次最多可读取10个云硬盘
  * sort_dir (String): 返回结果按照降序或升序排列。可选值:
    - desc: 降序
    - asc: 升序
    默认取值: desc
  * status (String): 云硬盘状态，取值可参考云硬盘状态文档
  * metadata (String): 云硬盘元数据
  * availability_zone (String): 可用区信息
  * multiattach (Boolean): 是否为共享云硬盘。可选值:
    - true: 表示为共享云硬盘
    - false: 表示为非共享云硬盘
  * service_type (String): 服务类型。可选值:
    - EVS: 云硬盘
    - DSS: 专属分布式存储服务
    - DESS: 专属企业存储服务
  * dedicated_storage_id (String): 专属存储池ID，可过滤出该专属存储池下的所有云硬盘，必须精确匹配
  * dedicated_storage_name (String): 专属存储池名称，可过滤出该专属存储池下的所有云硬盘，支持模糊匹配
  * volume_type_id (String): 云硬盘类型ID
  * id (String): 云硬盘ID
  * ids (String): 云硬盘ID列表，多个ID之间用逗号分隔
  * enterprise_project_id (String): 企业项目ID
  * server_id (String): 云服务器ID，可过滤出挂载到该云服务器下的所有云硬盘
  * server_ids (String): 云服务器ID列表，多个ID之间用逗号分隔
  * tags (String): 标签过滤，格式为 key=value。支持多标签查询，多个标签之间是"与"的关系
- 响应格式:
  * volumes (Array): 云硬盘列表，每个云硬盘对象包含以下主要字段:
    - id (String): 云硬盘ID，格式为UUID
    - name (String): 云硬盘名称
    - status (String): 云硬盘状态
    - attachments (Array): 挂载信息列表，每个挂载信息包含:
      * server_id (String): 云服务器ID
      * attachment_id (String): 挂载ID
      * device (String): 挂载点
      * host_name (String): 主机名
      * volume_id (String): 云硬盘ID
    - availability_zone (String): 可用区
    - bootable (String): 是否为启动盘，true表示启动盘，false表示数据盘
    - created_at (String): 创建时间，ISO8601格式
    - updated_at (String): 更新时间，ISO8601格式
    - description (String): 云硬盘描述
    - volume_type (String): 云硬盘类型
    - snapshot_id (String): 快照ID，如果云硬盘是从快照创建的，则显示快照ID
    - source_volid (String): 源云硬盘ID，如果云硬盘是从云硬盘克隆的，则显示源云硬盘ID
    - size (Integer): 云硬盘大小，单位为GiB
    - metadata (Object): 云硬盘元数据
    - multiattach (Boolean): 是否为共享云硬盘
    - encrypted (Boolean): 是否加密
    - iops (Object): IOPS信息，包含:
      * read_iops (Integer): 读IOPS
      * write_iops (Integer): 写IOPS
    - throughput (Object): 吞吐量信息，包含:
      * read_throughput (Integer): 读吞吐量，单位MB/s
      * write_throughput (Integer): 写吞吐量，单位MB/s
    - user_id (String): 用户ID
    - tenant_id (String): 租户ID
    - project_id (String): 项目ID
    - enterprise_project_id (String): 企业项目ID
    - service_type (String): 服务类型
    - dedicated_storage_id (String): 专属存储池ID
    - dedicated_storage_name (String): 专属存储池名称
    - tags (Array): 标签列表
    - wwn (String): 云硬盘的WWN（World Wide Name）
    - volume_image_metadata (Object): 云硬盘镜像元数据
    - os-vol-host-attr:host (String): 云硬盘所在的主机
    - os-vol-tenant-attr:tenant_id (String): 租户ID
    - os-vol-mig-status-attr:migstat (String): 迁移状态
    - os-vol-mig-status-attr:name_id (String): 迁移名称ID
    - shareable (Boolean): 是否可共享
    - replication_status (String): 复制状态
    - consistency_group_id (String): 一致性组ID
    - os-volume-replication:extended_status (String): 扩展复制状态
    - os-volume-replication:driver_data (String): 复制驱动数据
    - os-volume-replication:replication_type (String): 复制类型
    - os-volume-replication:replication_status (String): 复制状态
    - os-volume-replication:replication_extended_status (String): 复制扩展状态
    - os-volume-replication:replication_driver_data (String): 复制驱动数据
    - os-volume-replication:replication_type (String): 复制类型
    - links (Array): 链接列表，包含:
      * href (String): 链接地址
      * rel (String): 关系类型
  * count (Integer): 云硬盘总数
  * volumes_links (Array): 分页链接，包含:
    - rel (String): 关系类型，如 "next" 表示下一页
    - href (String): 链接地址
- 示例:
  * 查询所有云硬盘: GET /v2/{project_id}/cloudvolumes/detail
  * 按名称查询: GET /v2/{project_id}/cloudvolumes/detail?name=my-volume
  * 按状态查询: GET /v2/{project_id}/cloudvolumes/detail?status=available
  * 按可用区查询: GET /v2/{project_id}/cloudvolumes/detail?availability_zone=cn-north-1a
  * 查询共享云硬盘: GET /v2/{project_id}/cloudvolumes/detail?multiattach=true
  * 分页查询: GET /v2/{project_id}/cloudvolumes/detail?marker={volume_id}&limit=50
  * 使用offset分页: GET /v2/{project_id}/cloudvolumes/detail?offset=10&limit=20
  * 按创建时间排序: GET /v2/{project_id}/cloudvolumes/detail?sort_key=created_at&sort_dir=desc
  * 按大小排序: GET /v2/{project_id}/cloudvolumes/detail?sort_key=size&sort_dir=asc
  * 按云服务器ID查询: GET /v2/{project_id}/cloudvolumes/detail?server_id={server_id}
  * 按企业项目查询: GET /v2/{project_id}/cloudvolumes/detail?enterprise_project_id={ep_id}
  * 按标签查询: GET /v2/{project_id}/cloudvolumes/detail?tags=key1=value1
  * 按专属存储池查询: GET /v2/{project_id}/cloudvolumes/detail?dedicated_storage_id={storage_id}
  * 组合查询: GET /v2/{project_id}/cloudvolumes/detail?status=available&availability_zone=cn-north-1a&limit=50&sort_key=created_at&sort_dir=desc
