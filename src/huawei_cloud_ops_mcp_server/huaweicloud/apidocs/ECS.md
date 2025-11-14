ECS (弹性云服务器) API 文档:

常用端点:
1. 查询云服务器列表:
- action: 'v1.1/{project_id}/cloudservers/detail'
- method: GET
- 功能: 根据用户请求条件筛选、查询所有的弹性云服务器，并关联获取弹性云服务器的详细信息
- 路径参数:
  * project_id (必选): 项目ID
- 查询参数 (可选):
  * marker (String): 分页标记，以单页最后一条server的ID作为分页标记（推荐使用）
  * flavor_name (String): 云服务器规格名称，用于筛选特定规格的实例。已上线的规格请参见规格清单
  * name (String): 云服务器名称，支持模糊匹配。支持特殊字符，例如"."匹配除换行符之外的任何单个字符
  * status (String): 云服务器状态，可选值包括:
    - ACTIVE: 查询范围包括 ACTIVE、REBOOT、HARD_REBOOT、REBUILD、MIGRATING
    - SHUTOFF: 查询范围包括 SHUTOFF、RESIZE、REBUILD
    - ERROR: 查询范围包括 ERROR、REBUILD
    - VERIFY_RESIZE: 查询范围包括 VERIFY_RESIZE、REVERT_RESIZE
    - 其他状态: BUILD、HARD_REBOOT、MIGRATING、REBOOT、REBUILD、RESIZE、REVERT_RESIZE
  * limit (Integer): 查询返回云服务器列表当前页面的数量。每页默认值是10，最多返回100台云服务器的信息
  * tags (String): 标签过滤，格式为 key=value。支持多标签查询，多个标签之间是"与"的关系
  * ip (String): IP地址过滤，支持IPv4和IPv6地址
  * not-tags (String): 不包含指定标签的实例，格式为 key=value
  * enterprise_project_id (String): 企业项目ID
  * image (String): 镜像ID，用于筛选使用特定镜像的实例
  * flavor (String): 云服务器规格ID，用于筛选特定规格的实例
  * reservation_id (String): 预留实例ID
  * changes-since (String): 查询指定时间之后更新的云服务器，时间格式为ISO8601，例如: 2020-05-22T07:48:53Z
  * key_name (String): SSH密钥名称
  * user_id (String): 用户ID
  * locked (Boolean): 是否锁定，true表示锁定，false表示未锁定
  * sort_key (String): 排序字段，可选值: created_at, name, status, updated_at等
  * sort_dir (String): 排序方向，可选值: asc (升序), desc (降序)
- 响应格式:
  * servers (Array): 云服务器列表，每个服务器对象包含以下主要字段:
    - id (String): 云服务器ID，格式为UUID
    - name (String): 云服务器名称
    - status (String): 云服务器状态
    - vm_state (String): 虚拟机状态
    - task_state (String): 任务状态
    - flavor (Object): 规格信息，包含:
      * id (String): 规格ID
      * name (String): 规格名称
      * vcpus (Integer): CPU核数
      * ram (Integer): 内存大小(MB)
      * disk (Integer): 磁盘大小(GB)
      * gpus (Array): GPU信息
      * asic_accelerators (Array): ASIC加速器信息
    - availability_zone (String): 可用区
    - created (String): 创建时间，ISO8601格式
    - updated (String): 更新时间，ISO8601格式
    - tenant_id (String): 租户ID
    - user_id (String): 用户ID
    - in_recycle_bin (Boolean): 是否在回收站中
    - spod_id (String): 专属主机ID
    - metadata (Object): 元数据
    - addresses (Object): 网络地址信息
    - volumes_attached (Array): 挂载的云硬盘列表，每个卷包含:
      * id (String): 磁盘ID，格式为UUID
      * delete_on_termination (Boolean): 删除云服务器时是否一并删除该磁盘
      * bootIndex (String): 云硬盘启动顺序，0为系统盘，非0为数据盘
      * device (String): 云硬盘挂载盘符，即磁盘挂载点
      * size (Integer): 云盘大小，单位为GiB
    - security_groups (Array): 安全组列表
    - fault (Object): 错误信息（如果存在），包含:
      * code (Integer): 错误码
      * created (String): 异常出现的时间，ISO8601格式
      * message (String): 异常描述信息
      * details (String): 异常详细信息
    - locked (Boolean): 是否锁定
    - tags (Array): 标签列表
    - enterprise_project_id (String): 企业项目ID
    - sys_tags (Array): 系统标签列表
    - cpu_options (Object): CPU选项，包含 hw:cpu_threads (Integer): CPU超线程设置，1表示关闭，2表示打开
    - billed (String): 计费方式，可选值: PrePaid (包年/包月), PostPaid (按需)
    - charged (Boolean): 是否已计费
    - expired_time (String): 包年/包月云服务器计费到期时间，ISO8601格式
  * servers_links (Array): 分页链接，包含:
    - rel (String): 关系类型，如 "next" 表示下一页
    - href (String): 链接地址
  * request_id (String): 请求ID
- 示例:
  * 查询所有实例: GET /v1.1/{project_id}/cloudservers/detail
  * 按名称模糊查询: GET /v1.1/{project_id}/cloudservers/detail?name=test
  * 按状态查询: GET /v1.1/{project_id}/cloudservers/detail?status=ACTIVE
  * 按规格查询: GET /v1.1/{project_id}/cloudservers/detail?flavor_name=s2.medium.2
  * 分页查询: GET /v1.1/{project_id}/cloudservers/detail?marker={server_id}&limit=50
  * 标签过滤: GET /v1.1/{project_id}/cloudservers/detail?tags=key1=value1
  * 组合查询: GET /v1.1/{project_id}/cloudservers/detail?status=ACTIVE&limit=20&sort_key=created_at&sort_dir=desc
