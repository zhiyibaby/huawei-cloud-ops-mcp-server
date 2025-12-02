OBS (对象存储服务) API 文档:

常用端点:
1. 查询桶列表:
- action: '/'
- method: GET
- 功能: 查询用户创建的所有区域的桶列表
- 路径参数: 无
- 查询参数: 无
- 请求头 (可选):
  * x-obs-bucket-type (String): 明确获取桶列表的内容，即列表中包含什么类型的桶
    - 取值范围:
      - OBJECT: 获取所有对象桶列表
      - POSIX: 获取所有并行文件系统列表
    - 默认取值: 不带此请求头则获取所有桶和并行文件系统列表
    - 示例: x-obs-bucket-type: POSIX
  * x-obs-ies-location (String): 列举指定AZ Id的CloudPond站点的桶，普通桶不返回
    - 约束限制: 必须携带合法的CloudPond站点的AZ Id，否则无法列出桶
    - 示例: x-obs-ies-location: AZ1
  * x-obs-edge-location (String): 列举指定AZ Id的智能边缘云站点的桶，普通桶不返回
    - 约束限制: 必须携带合法的智能边缘云站点的AZ Id，否则无法列出桶
    - 示例: x-obs-edge-location: AZ1
- 响应格式 (XML):
  * ListAllMyBucketsResult: 根元素
    - Owner: 桶的所有者信息
      * ID (String): 用户ID
    - Buckets: 桶列表
      * Bucket (Array): 桶对象列表，每个桶包含:
        - Name (String): 桶名称
        - CreationDate (String): 桶的创建时间（UTC时间），日期格式为ISO8601，例如: 2025-06-28T08:57:41.047Z
        - Location (String): 桶所在的区域，例如: cn-north-4
        - BucketType (String): 桶类型
          * OBJECT: 对象存储桶
          * POSIX: 并行文件系统
        - IESLocation (String, 可选): CloudPond桶所在站点的AZ Id，非CloudPond的桶不存在此标签
        - EdgeLocation (String, 可选): 智能边缘云的桶所在站点的AZ Id，非智能边缘云的桶不存在此标签
- 接口约束:
  * 终端节点（Endpoint）不会限制查询结果，无论哪一个区域的Endpoint，查询结果都是所有区域的桶列表
  * 创建桶时，请勿并发列举桶
- 示例:
  * 查询所有桶: GET / (不带任何请求头)
  * 查询对象桶列表: GET / (请求头: x-obs-bucket-type: OBJECT)
  * 查询并行文件系统列表: GET / (请求头: x-obs-bucket-type: POSIX)
  * 查询CloudPond站点桶: GET / (请求头: x-obs-ies-location: AZ1)
  * 查询智能边缘云站点桶: GET / (请求头: x-obs-edge-location: AZ1)

