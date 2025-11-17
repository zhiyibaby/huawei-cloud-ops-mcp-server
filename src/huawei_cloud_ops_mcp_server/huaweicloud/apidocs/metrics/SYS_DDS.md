SYS.DDS (文档数据库服务监控指标) 监控指标文档:

命名空间: SYS.DDS

说明: DDS服务上报云监控服务的监控指标，用于监控文档数据库服务实例的性能指标。云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级。例如监控指标中的维度信息为"mongodb_instance_id,mongodb_node_id"时，表示对应的监控指标的维度存在层级关系，且"mongodb_instance_id"为0层，"mongodb_node_id"为1层。

## DDS推荐的监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 测量对象 | 监控周期（原始指标） |
|--------|----------|----------|----------|------|------|------|----------|---------------------|
| mongo007_connections_usage | 当前活动连接数百分比 | 该指标用于统计试图连接到实例节点的连接数占可用连接数百分比。 | 0~100 | % | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds mongos节点 文档数据库实例下的主节点 文档数据库实例下的备节点 | 1分钟 5秒 |
| mongo032_mem_usage | 内存使用率 | 该指标用于统计测量对象的内存利用率。 | 0~100 | % | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds mongos节点 文档数据库实例下的主节点 文档数据库实例下的备节点 | 1分钟 5秒 |
| mongo031_cpu_usage | CPU使用率 | 该指标用于统计测量对象的CPU利用率。 | 0~100 | % | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds mongos节点 文档数据库实例下的主节点 文档数据库实例下的备节点 | 1分钟 5秒 |
| mongo035_disk_usage | 磁盘利用率 | 该指标用于统计测量对象的磁盘利用率。 | 0~100 | % | 不涉及 | mongodb_node_id | 文档数据库实例下的主节点 文档数据库实例下的备节点 | 1分钟 |

## DDS支持的监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 测量对象 | 监控周期（原始指标） |
|--------|----------|----------|----------|------|------|------|----------|---------------------|
| mongo001_command_ps | command执行频率 | 该指标用于统计平均每秒command语句在节点上执行次数。 | ≥ 0 | Count/s | 不涉及 | mongodb_instance_id,mongodb_node_id | 文档数据库实例 文档数据库集群实例下的dds mongos节点 文档数据库副本集实例下的只读节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 5秒 |
| mongo002_delete_ps | delete语句执行频率 | 该指标用于统计平均每秒delete语句在节点上执行次数。 | ≥ 0 | Count/s | 不涉及 | mongodb_instance_id,mongodb_node_id | 文档数据库实例 文档数据库集群实例下的dds mongos节点 文档数据库副本集实例下的只读节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 5秒 |
| mongo106_command_time_p99 | command p99耗时 | 该指标为单个节点的command耗时p99耗时。 | ≥ 0 | ms | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds shard节点 文档数据库集群实例下的dds config节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 |
| mongo107_command_time_p999 | command p999耗时 | 该指标为单个节点的command耗时p999耗时。 | ≥ 0 | ms | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds shard节点 文档数据库集群实例下的dds config节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 |
| mongo108_txn_time_average | 事务耗时平均值 | 该指标为单个节点的节点事务耗时平均值。 | ≥ 0 | ms | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds shard节点 文档数据库集群实例下的dds config节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 |
| mongo109_txn_time_p99 | 事务p99耗时 | 该指标为单个节点的事务p99耗时。 | ≥ 0 | ms | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds shard节点 文档数据库集群实例下的dds config节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 |
| mongo110_txn_time_p999 | 事务p999耗时 | 该指标为单个节点的事务p999耗时。 | ≥ 0 | ms | 不涉及 | mongodb_node_id | 文档数据库集群实例下的dds shard节点 文档数据库集群实例下的dds config节点 文档数据库实例下的主节点 文档数据库实例下的备节点 文档数据库实例下的隐藏节点 | 1分钟 |

注意: 指标ID中含有"rocks"的监控指标均用于监测4.2版本的实例或实例节点。

## 维度说明

| 维度名称 | 维度含义 |
|----------|----------|
| mongodb_instance_id | 文档数据库实例ID。支持社区版集群、副本集、以及单节点实例类型。 |
| mongodb_node_id | 文档数据库节点ID。 |

说明: mongodb_instance_id维度用于调用CES API时指定维度字段，并不表示所有类型的实例都有实例级别的指标，副本集和单节点类型没有实例级别的指标。

## 使用说明

1. 命名空间: SYS.DDS
2. 监控周期: 1分钟、5秒（原始指标，具体指标支持的周期不同）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询DDS实例节点的磁盘利用率（mongo035_disk_usage），该指标的维度信息为"mongodb_instance_id,mongodb_node_id"，表示mongodb_instance_id为0层，mongodb_node_id为1层
   - 通过CES接口查询单个监控指标时: dim.0=mongodb_instance_id,{mongodb_instance_id值}&dim.1=mongodb_node_id,{mongodb_node_id值}
   - 通过CES接口批量查询监控指标时: "dimensions": [{"name": "mongodb_instance_id", "value": "{mongodb_instance_id值}"}, {"name": "mongodb_node_id", "value": "{mongodb_node_id值}"}]

