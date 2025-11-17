CES (云监控服务) API 文档:

常用端点:
1. 查询监控数据:
- action: 'V1.0/{project_id}/metric-data'
- method: GET
- 功能: 查询指定时间范围指定指标的指定粒度的监控数据，可以通过参数指定需要查询的数据维度
- 路径参数:
  * project_id (必选): 项目ID，用于明确项目归属，配置后可通过该ID查询项目下资产
- 查询参数:
  * namespace (必选, String): 服务指标命名空间。各服务命名空间请参考支持监控的服务列表
    - 格式: service.item，service和item必须是字符串，必须以字母开头，只能包含0-9/a-z/A-Z/_，其中service不能为"SYS"、"AGT"和"SRE"，namespace不能为SERVICE.BMS
    - 字符串长度在3~32之间
    - 示例: AGT.ECS (弹性云服务器), SYS.DDS (文档数据库), SYS.CloudTable (表格存储服务)
  * metric_name (必选, String): 指标ID，例如弹性云服务器的监控指标CPU使用率，对应的metric_name为cpu_util
    - 必须以字母开头，只能包含0-9/a-z/A-Z/_/-
    - 字符串长度在1~96之间
    - 示例: cpu_util (CPU使用率), mongo001_command_ps (command执行频率), cmdProcessMem (进程内存)
  * dim.{i} (必选, String): 维度参数，用于指定监控对象的维度信息，格式为 key,value
    - i 从0开始递增，表示第几个维度，只支持4个维度
    - 格式: dim.0=key1,value1&dim.1=key2,value2
    - 示例: dim.0=instance_id,12345678-1234-1234-1234-123456789012
    - 示例: dim.0=cluster_id,f2fbxxxc-36b2-4d1d-895d-972a4d656xxx&dim.1=instance_name,hmaster-active
    - 注意: 必须至少提供一个维度参数 dim.0，用于标识具体的监控对象
  * from (必选, Long): 查询数据起始时间，UNIX时间戳，单位毫秒
    - 示例: 1556625600000 (对应 2019-04-30 20:00:00)
  * to (必选, Long): 查询数据结束时间，UNIX时间戳，单位毫秒
    - 示例: 1556632800000 (对应 2019-04-30 22:00:00)
    - 注意: to 必须大于 from
  * period (必选, Integer): 监控数据粒度，单位秒
    - 可选值: 1, 300, 1200, 3600, 14400, 86400
    - 1: 原始数据
    - 300: 5分钟粒度
    - 1200: 20分钟粒度
    - 3600: 1小时粒度
    - 14400: 4小时粒度
    - 86400: 1天粒度
    - 注意: 必须指定 period 参数，系统不会自动选择粒度
  * filter (必选, String): 聚合方式，指定返回数据的聚合类型
    - 可选值: average (平均值), max (最大值), min (最小值), sum (求和值), variance (方差)
    - 注意: 必须指定 filter 参数，且只能指定一个聚合方式，不能同时指定多个
- 响应格式:
  * datapoints (Array of objects): 指标数据列表，每个数据点包含以下字段:
    - average (Double, 可选): 聚合周期内指标数据的平均值
    - max (Double, 可选): 聚合周期内指标数据的最大值
    - min (Double, 可选): 聚合周期内指标数据的最小值
    - sum (Double, 可选): 聚合周期内指标数据的求和值
    - variance (Double, 可选): 聚合周期内指标数据的方差
    - timestamp (Long): 指标采集时间，UNIX时间戳，单位毫秒
    - unit (String): 指标单位，如 "%", "Bytes", "Count" 等
    - 注意: 由于查询数据时，云监控会根据所选择的聚合粒度向前取整from参数，所以datapoints中包含的数据点有可能会多于预期
  * metric_name (String): 指标ID，例如弹性云服务器监控指标中的cpu_util
- 示例:
  * 查询弹性云服务器CPU使用率平均值:
    GET /V1.0/{project_id}/metric-data?namespace=SYS.ECS&metric_name=cpu_util&dim.0=instance_id,12345678-1234-1234-1234-123456789012&from=1442341200000&to=1442344800000&period=300&filter=average
  * 查询弹性云服务器CPU使用率最大值:
    GET /V1.0/{project_id}/metric-data?namespace=SYS.ECS&metric_name=cpu_util&dim.0=instance_id,12345678-1234-1234-1234-123456789012&from=1442341200000&to=1442344800000&period=300&filter=max
  * 查询指定实例的监控数据:
    GET /V1.0/{project_id}/metric-data?namespace=SYS.ECS&metric_name=cpu_util&dim.0=instance_id,12345678-1234-1234-1234-123456789012&from=1442341200000&to=1442344800000&period=300&filter=average
  * 查询表格存储服务进程内存监控数据:
    GET /V1.0/{project_id}/metric-data?namespace=SYS.CloudTable&metric_name=cmdProcessMem&dim.0=cluster_id,f2fbxxxc-36b2-4d1d-895d-972a4d656xxx&dim.1=instance_name,hmaster-active&from=1556625600000&to=1556632800000&period=1200&filter=variance
  * 查询最小值:
    GET /V1.0/{project_id}/metric-data?namespace=SYS.ECS&metric_name=cpu_util&dim.0=instance_id,12345678-1234-1234-1234-123456789012&from=1442341200000&to=1442344800000&period=300&filter=min
- 常见命名空间和指标:
  * AGT.ECS (弹性云服务器): [AGT_ECS.md](metrics/AGT_ECS.md)
  * SYS.EVS (云硬盘-仅当挂载到云服务器时): [SYS_EVS.md](metrics/SYS_EVS.md)
  * SYS.VPC (虚拟私有云): [SYS_VPC.md](metrics/SYS_VPC.md)
  * SYS.DCS (分布式缓存服务): [SYS_DCS.md](metrics/SYS_DCS.md)
  * SYS.RDS (关系型数据库MySQL): [SYS_RDS.md](metrics/SYS_RDS.md)
  * SYS.ES (云搜索服务): [SYS_ES.md](metrics/SYS_ES.md)
  * SYS.DDS (文档数据库): [SYS_DDS.md](metrics/SYS_DDS.md)
- 注意事项:
  * 时间范围限制: 查询时间范围不能超过30天
  * 数据保留期: 原始数据保留7天，聚合数据保留30天
  * 维度参数: dim.{i} 是必选参数，必须至少提供一个维度参数 dim.0 来标识具体的监控对象，必须确保维度值的准确性，否则可能查询不到数据
  * 聚合粒度: period 是必选参数，必须明确指定监控数据粒度，系统不会自动选择
  * 聚合方式: filter 是必选参数，必须明确指定一个聚合方式（如 average, max, min, sum, variance），不能同时指定多个聚合方式
  * 时区: 所有时间戳均为UTC时间，需要根据实际时区进行转换