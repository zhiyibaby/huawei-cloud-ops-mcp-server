LTS (云日志服务) API 文档:

常用端点:
1. 查询账号下所有日志组:
- action: 'v2/{project_id}/groups'
- method: GET
- 功能: 查询账号下所有日志组。通过调用该接口可快速查询指定账号下的日志组列表，以及该账号下所创建的每一个日志组信息，为您全面掌握账号内的日志管理和资源分布情况提供有力支持
- 路径参数:
  * project_id (必选): 项目ID，可以从调用API处获取，也可以从控制台获取
- 请求Header参数:
  * Content-Type (必选): 用于定义消息体的格式，该字段填为：application/json;charset=utf8
- 响应格式:
  * log_groups (Array): 日志组信息列表，每个日志组对象包含以下主要字段:
    - creation_time (Long): 日志组创建时间，时间戳格式（毫秒）
    - log_group_name (String): 日志组名称
    - log_group_id (String): 日志组ID
    - ttl_in_days (Integer): 日志组的存储时间，即日志上报到LTS后日志存储的时间（单位：天）
    - tag (Map<String,String>): 日志组标签信息。标签是以键值对（key-value）的形式表示，key和value为一一对应关系
    - log_group_name_alias (String): 日志组别名
- 示例:
  * 查询所有日志组: GET /v2/{project_id}/groups
  * 完整请求示例: GET https://{endpoint}/v2/{project_id}/groups

2. 查询指定日志组下的所有日志流:
- action: 'v2/{project_id}/groups/{log_group_id}/streams'
- method: GET
- 功能: 查询指定日志组下的所有日志流信息。通过该接口可以获取指定日志组下的所有日志流详情，详细展示每条日志的具体情况，为您提供日志流信息查询方式，满足日志管理的多样化需求
- 路径参数:
  * project_id (必选): 项目ID，可以从调用API处获取，也可以从控制台获取
  * log_group_id (必选): 日志组ID
- 请求Header参数:
  * Content-Type (必选): 用于定义消息体的格式，该字段填为：application/json;charset=utf8
- 响应格式:
  * log_streams (Array): 日志流相关配置信息列表，每个日志流对象包含以下主要字段:
    - creation_time (Long): 日志流创建时间。UNIX 时间戳格式，表示从1970-1-1 00:00:00 UTC计算起的毫秒数
    - log_stream_name (String): 日志流名称
    - log_stream_id (String): 日志流ID
    - log_stream_name_alias (String): 日志流别名
    - ttl_in_days (Integer): 日志流的存储时间，即日志上报到LTS后日志存储的时间（单位：天），-1表示永久存储
    - tag (Map<String,String>): 日志流标签信息。标签是以键值对（key-value）的形式表示，key和value为一一对应关系
    - auth_web_tracking (Boolean): 是否启用Web追踪认证
    - is_favorite (Boolean): 是否收藏
    - hot_storage_days (Integer): 热存储天数，-1表示未启用热存储
    - hot_cold_separation (Boolean): 是否启用冷热分离
    - filter_count (Integer): 过滤器数量
    - whether_log_storage (Boolean): 是否启用日志存储
- 示例:
  * 查询指定日志组下的所有日志流: GET /v2/{project_id}/groups/{log_group_id}/streams
  * 完整请求示例: GET https://{endpoint}/v2/{project_id}/groups/{log_group_id}/streams

3. 查询指定日志流下的日志内容 (ListLogs):
- action: 'v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/content/query'
- method: POST
- 功能: 查询指定日志流下的日志内容。通过调用该接口可以查询指定日志流中的日志数据，支持按时间范围、关键字、字段等条件进行过滤查询，满足日志检索和分析的多样化需求
- 路径参数:
  * project_id (必选): 项目ID，可以从调用API处获取，也可以从控制台获取
  * log_group_id (必选): 日志组ID
  * log_stream_id (必选): 日志流ID
- 请求Header参数:
  * Content-Type (必选): 用于定义消息体的格式，该字段填为：application/json;charset=utf8
- 请求Body参数:
  * start_time (必选, String): 按照时间范围搜索日志的起始时间。日志时间为日志数据写入时的时间。参数start_time和end_time组成的时间区间，既包含起始时间也包含结束时间。查询时间区间最大为180天。start_time和end_time取值不能相同。取值范围：毫秒级时间戳，表示从1970-1-1 00:00:00 UTC开始计算的毫秒数
  * end_time (必选, String): 按照时间范围搜索日志的结束时间。日志时间为日志数据写入时的时间。参数start_time和end_time组成的时间区间，既包含起始时间也包含结束时间。查询时间区间最大为180天。start_time和end_time取值不能相同。取值范围：毫秒级时间戳，表示从1970-1-1 00:00:00 UTC开始计算的毫秒数
  * labels (可选, Map<String,String>): 指定字段名称和字段值（key:value）的过滤条件集合进行搜索。可以使用内置保留字段，如果想要配置更多字段，需要调用创建日志流索引接口配置字段索引
  * query (可选, String): 查询语句，支持LTS查询语法。例如: "* | select field1,field2 from log", 当is_analysis_query为true时生效
  * keywords (可选, String): 支持关键词精确搜索。关键词指相邻两个分词符之间的单词，例如：error
  * is_analysis_query (可选, Boolean): 是否为分析查询。true表示分析查询，false表示搜索查询。默认为false
  * highlight (可选, Boolean): 是否高亮显示匹配的日志内容。默认为false
  * line_num (可选, String): 行号，用于定位日志在日志流中的位置
  * search_type (可选, String): 搜索类型，可选值包括: normal (普通搜索), regex (正则搜索), fuzzy (模糊搜索)。默认为normal
  * is_desc (可选, Boolean): 表示日志查询的顺序，当前支持顺序（false）或倒序查询（true），默认为false
  * is_count (可选, Boolean): 在查询结果中是否统计日志条数，默认为false
  * limit (可选, Integer): 返回日志条数限制，最大值为10000。默认为100
  * from (可选, Integer): 起始位置，用于分页查询。默认为0
  * to (可选, Integer): 结束位置，用于分页查询。通常使用from和limit进行分页，to参数较少使用
- 响应格式:
  * logs (Array): 日志内容列表，每个日志对象包含以下主要字段:
    - time (Long): 日志时间戳，毫秒级时间戳，表示从1970-1-1 00:00:00 UTC开始计算的毫秒数
    - content (String): 日志内容，原始日志文本
    - line_num (String): 行号，用于定位日志在日志流中的位置
    - labels (Map<String,String>): 日志标签信息，包含日志的元数据字段和值
    - highlight (Object, 可选): 高亮信息（如果启用高亮），包含匹配字段的高亮标记
  * total (Integer, 可选): 符合条件的日志总数。当is_count为true时返回此字段
  * result_count (Integer, 可选): 本次查询返回的日志条数
- 接口约束:
  * 查询时间区间最大为180天
  * start_time和end_time取值不能相同
  * limit最大值为10000
  * 需要先创建日志流索引才能使用labels字段进行过滤查询
  * 当is_analysis_query为true时，query参数生效，keywords参数不生效
  * 当is_analysis_query为false时，可以使用keywords进行关键词搜索
  * keywords和query不能同时使用
- 示例:
  * 查询指定日志流下的日志内容: POST /v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/content/query
  * 完整请求示例: POST https://{endpoint}/v2/{project_id}/groups/{log_group_id}/streams/{log_stream_id}/content/query
  * 请求Body示例（基础查询）:
    {
      "start_time": "1722324332801",
      "end_time": "1722327932801",
      "limit": 100
    }
  * 请求Body示例（分析查询）:
    {
      "start_time": "1722324332801",
      "end_time": "1722327932801",
      "query": "* | select field1,field2 from log",
      "is_analysis_query": true,
      "limit": 100
    }
  * 请求Body示例（带标签过滤）:
    {
      "start_time": "1722324332801",
      "end_time": "1722327932801",
      "labels": {
        "level": "ERROR",
        "service": "api"
      },
      "search_type": "normal",
      "is_desc": true,
      "is_count": true,
      "limit": 50
    }
  * 请求Body示例（关键词搜索）:
    {
      "start_time": "1722324332801",
      "end_time": "1722327932801",
      "keywords": "error",
      "is_desc": true,
      "highlight": true,
      "limit": 100
    }
