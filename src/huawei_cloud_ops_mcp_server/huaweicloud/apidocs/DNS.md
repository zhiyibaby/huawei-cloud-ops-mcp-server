DNS (云解析服务) API 文档:

常用端点:
1. 查询公网域名列表:
- action: '/v2/zones'
- method: GET
- 功能: 当您的公网域名创建成功后，您可以通过调用此接口查询所有公网域名信息，包括域名、ID、状态、记录集个数、企业项目、标签、TTL、创建时间、修改时间、描述等
- 注意: 公网域名为全局资源，请选择"华北-北京四（cn-north-4）"区域调用
- 查询参数 (可选):
  * type (String): 待查询域名的类型。取值范围: public（公网域名）。默认值: public
  * limit (Integer): 分页查询时配置每页返回的资源个数。取值范围: 0~500。默认值: 500
  * marker (String): 分页查询的起始资源ID。查询第一页时，设置为空。查询下一页时，设置为上一页最后一条资源的ID
  * offset (Integer): 分页查询起始偏移量，表示从偏移量的下一个资源开始查询。当设置marker不为空时，以marker为分页起始标识，offset不生效。取值范围: 0~2147483647。默认值: 0
  * tags (String): 公网域名的标签，包括标签键和标签值。取值格式: key1,value1|key2,value2。多个标签之间用"|"分开，每个标签的键值用英文逗号","相隔。多个标签之间为"与"的关系。搜索模式为精确搜索。如果资源标签值value是以*开头时，则按照*后面的值全模糊匹配。最多可以查询20个标签
  * name (String): 域名。搜索模式默认为模糊搜索
  * id (String): 域名ID
  * status (String): 公网域名状态，可选值包括:
    - ACTIVE: 正常
    - PENDING_CREATE: 创建中
    - PENDING_UPDATE: 更新中
    - PENDING_DELETE: 删除中
    - PENDING_FREEZE: 冻结中
    - FREEZE: 冻结
    - ILLEGAL: 违规冻结
    - POLICE: 公安冻结
    - PENDING_DISABLE: 暂停中
    - DISABLE: 暂停
    - ERROR: 失败
  * search_mode (String): 查询条件搜索模式。取值范围: like（模糊搜索）、equal（精确搜索）
  * sort_key (String): 查询结果中域名列表的排序字段。取值范围: name（域名）、created_at（创建时间）、updated_at（更新时间）。默认值: created_at
  * sort_dir (String): 查询结果中域名列表的排序方式。取值范围: desc（降序排序）、asc（升序排序）。默认值: desc
  * enterprise_project_id (String): 域名所属的企业项目ID。可以使用该字段过滤企业项目下的域名。最大长度36字节，带"-"连字符的UUID格式，或者是字符串"0"（"0"表示默认企业项目）。默认值: 0
- 响应格式:
  * zones (Array): 公网域名列表，每个域名对象包含以下主要字段:
    - id (String): 域名ID，格式为UUID
    - name (String): 域名名称
    - description (String): 域名的描述信息
    - email (String): 管理该域名的邮箱地址
    - zone_type (String): 域名类型，public表示公网域名
    - ttl (Integer): 解析记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位
    - serial (Integer): 序列号，用于标识该域名的版本
    - status (String): 资源状态
    - record_num (Integer): 该域名下的解析记录个数
    - pool_id (String): 域名关联的DNS服务池ID
    - project_id (String): 项目ID
    - enterprise_project_id (String): 企业项目ID
    - created_at (String): 创建时间，ISO8601格式
    - updated_at (String): 更新时间，ISO8601格式
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
    - masters (Array): 主域名服务器列表
    - links (Object): 资源链接信息，包含:
      * self (String): 当前资源的链接
      * next (String): 下一页资源的链接（如果存在）
  * links (Object): 分页链接信息，包含:
    - self (String): 当前页链接
    - next (String): 下一页链接（如果存在）
  * metadata (Object): 分页元数据，包含:
    - total_count (Integer): 资源总数
  * request_id (String): 请求ID
- 示例:
  * 查询所有公网域名: GET /v2/zones?type=public
  * 按名称模糊查询: GET /v2/zones?name=example
  * 按状态查询: GET /v2/zones?status=ACTIVE
  * 按域名ID查询: GET /v2/zones?id={zone_id}
  * 分页查询: GET /v2/zones?marker={zone_id}&limit=50
  * 标签过滤: GET /v2/zones?tags=key1,value1|key2,value2
  * 组合查询: GET /v2/zones?status=ACTIVE&limit=20&sort_key=created_at&sort_dir=desc
  * 企业项目过滤: GET /v2/zones?enterprise_project_id={ep_id}
  * 精确搜索: GET /v2/zones?name=example.com&search_mode=equal

2. 查询域名下的记录集列表:
- action: '/v2/zones/{zone_id}/recordsets'
- method: GET
- 功能: 当您的记录集创建成功后，您可以通过调用此接口查询指定域名下的所有记录集信息，包括名称、ID、状态、所属域名、解析记录值、标签、TTL、创建时间、修改时间、描述等
- 路径参数 (必选):
  * zone_id (String): 域名ID
- 查询参数 (可选):
  * search_mode (String): 查询条件搜索模式。取值范围: like（模糊搜索）、equal（精确搜索）
  * marker (String): 分页查询的起始资源ID。查询第一页时，设置为空。查询下一页时，设置为上一页最后一条资源的ID
  * limit (Integer): 分页查询时配置每页返回的资源个数。取值范围: 0~500。默认值: 500
  * offset (Integer): 分页查询起始偏移量，表示从偏移量的下一个资源开始查询。当设置marker不为空时，以marker为分页起始标识，offset不生效。取值范围: 0~2147483647。默认值: 0
  * tags (String): 记录集的标签，包括标签键和标签值。取值格式: key1,value1|key2,value2。多个标签之间用"|"分开，每个标签的键值用英文逗号","相隔。多个标签之间为"与"的关系。搜索模式为精确搜索。如果资源标签值value是以*开头时，则按照*后面的值全模糊匹配。最多可以查询20个标签
  * status (String): 记录集状态，可选值包括:
    - ACTIVE: 正常
    - PENDING_CREATE: 创建中
    - PENDING_UPDATE: 更新中
    - PENDING_DELETE: 删除中
    - PENDING_FREEZE: 冻结中
    - FREEZE: 冻结
    - ILLEGAL: 违规冻结
    - POLICE: 公安冻结
    - PENDING_DISABLE: 暂停中
    - DISABLE: 暂停
    - ERROR: 失败
  * type (String): 记录集的类型。公网域名的记录类型: A、AAAA、MX、CNAME、TXT、SRV、NS、SOA、CAA。内网域名的记录类型: A、AAAA、MX、CNAME、TXT、PTR、SRV、NS、SOA
  * name (String): 待查询的记录集的域名中包含此name。搜索模式默认为模糊搜索
  * id (String): 待查询的记录集ID
  * sort_key (String): 查询结果中记录集列表的排序字段。取值范围: name（记录集名称）、type（记录集类型）。默认值: 空（不排序）
  * sort_dir (String): 查询结果中记录集列表的排序方式。取值范围: desc（降序排序）、asc（升序排序）。默认值: 空（不排序）
- 响应格式:
  * recordsets (Array): 记录集列表，每个记录集对象包含以下主要字段:
    - id (String): 记录集ID，格式为UUID
    - name (String): 记录集名称
    - description (String): 记录集的描述信息
    - zone_id (String): 所属域名ID
    - zone_name (String): 所属域名名称
    - type (String): 记录集类型
    - ttl (Integer): 解析记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位
    - records (Array): 解析记录值列表
    - status (String): 资源状态
    - default (Boolean): 是否为默认记录集
    - project_id (String): 项目ID
    - created_at (String): 创建时间，ISO8601格式
    - updated_at (String): 更新时间，ISO8601格式
    - links (Object): 资源链接信息，包含:
      * self (String): 当前资源的链接
      * next (String): 下一页资源的链接（如果存在）
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
  * links (Object): 分页链接信息，包含:
    - self (String): 当前页链接
    - next (String): 下一页链接（如果存在）
  * metadata (Object): 分页元数据，包含:
    - total_count (Integer): 资源总数
  * request_id (String): 请求ID
- 示例:
  * 查询指定域名的所有记录集: GET /v2/zones/{zone_id}/recordsets
  * 按名称模糊查询: GET /v2/zones/{zone_id}/recordsets?name=www
  * 按类型查询: GET /v2/zones/{zone_id}/recordsets?type=A
  * 按状态查询: GET /v2/zones/{zone_id}/recordsets?status=ACTIVE
  * 按记录集ID查询: GET /v2/zones/{zone_id}/recordsets?id={recordset_id}
  * 分页查询: GET /v2/zones/{zone_id}/recordsets?marker={recordset_id}&limit=50
  * 标签过滤: GET /v2/zones/{zone_id}/recordsets?tags=key1,value1|key2,value2
  * 组合查询: GET /v2/zones/{zone_id}/recordsets?type=A&status=ACTIVE&limit=20&sort_key=name&sort_dir=asc
  * 精确搜索: GET /v2/zones/{zone_id}/recordsets?name=www.example.com&search_mode=equal