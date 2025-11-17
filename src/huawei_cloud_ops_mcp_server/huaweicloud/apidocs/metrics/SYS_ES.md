SYS.ES (云搜索服务 Elasticsearch 监控指标) 监控指标文档:

命名空间: SYS.ES

说明: 云搜索服务上报云监控服务的监控指标，用于监控Elasticsearch集群的性能指标。监控周期为1分钟。云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级。累计值：从节点启动时开始叠加数值，当节点重启后清零重新累计。

## Elasticsearch集群监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期（原始指标） |
|--------|----------|----------|----------|------|------|------|---------------------|
| status | 集群健康状态 | 该指标用于统计测量监控对象的状态。0：集群是100%可用的。1：数据是完整的，部分副本缺失。高可用性在某种程度上弱化，存在风险，请及时关注集群情况。2：数据缺失，集群使用时将出现异常。3：没有获取到集群状态。 | 0、1、2、3 | 不涉及 | 不涉及 | cluster_id | 1分钟 |
| disk_util | 最大磁盘使用率 | CSS集群中各个节点的磁盘使用率的最大值。 | 0~100 | % | 不涉及 | cluster_id | 1分钟 |
| max_jvm_heap_usage | 最大JVM堆使用率 | CSS集群中各个节点的JVM堆使用率的最大值。 | 0~100 | % | 不涉及 | cluster_id | 1分钟 |
| max_jvm_young_gc_time | 最大JVM Young GC耗时 | CSS集群中各个节点的JVM Young GC耗时累计值的最大值。 | ≥ 0 | ms | 不涉及 | cluster_id | 1分钟 |
| max_jvm_young_gc_count | 最大JVM Young GC次数 | CSS集群中各个节点的JVM Young GC次数累计值的最大值。 | ≥ 0 | Count | 不涉及 | cluster_id | 1分钟 |
| max_jvm_old_gc_time | 最大JVM Old GC耗时 | CSS集群中各个节点的JVM Old GC耗时累计值的最大值。 | ≥ 0 | ms | 不涉及 | cluster_id | 1分钟 |
| max_jvm_old_gc_count | 最大JVM Old GC次数 | CSS集群中各个节点的JVM Old GC次数累计值的最大值。 | ≥ 0 | Count | 不涉及 | cluster_id | 1分钟 |
| cpu_usage | CPU使用率 | 该指标用于统计测量对象的CPU使用率。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |
| mem_usage | 内存使用率 | 该指标用于统计测量对象的内存使用率。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |
| disk_read_rate | 磁盘读速率 | 该指标用于统计测量对象的磁盘读速率。 | ≥ 0 | bytes/s | 不涉及 | cluster_id,instance_id | 1分钟 |
| disk_write_rate | 磁盘写速率 | 该指标用于统计测量对象的磁盘写速率。 | ≥ 0 | bytes/s | 不涉及 | cluster_id,instance_id | 1分钟 |
| network_incoming_bytes_rate | 网络入流量 | 该指标用于统计测量对象的网络入流量。 | ≥ 0 | bytes/s | 不涉及 | cluster_id,instance_id | 1分钟 |
| network_outgoing_bytes_rate | 网络出流量 | 该指标用于统计测量对象的网络出流量。 | ≥ 0 | bytes/s | 不涉及 | cluster_id,instance_id | 1分钟 |
| jvm_heap_usage | JVM堆使用率 | 该指标用于统计测量对象的JVM堆使用率。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |
| jvm_young_gc_time | JVM Young GC耗时 | 该指标用于统计测量对象的JVM Young GC耗时累计值。 | ≥ 0 | ms | 不涉及 | cluster_id,instance_id | 1分钟 |
| jvm_young_gc_count | JVM Young GC次数 | 该指标用于统计测量对象的JVM Young GC次数累计值。 | ≥ 0 | Count | 不涉及 | cluster_id,instance_id | 1分钟 |
| jvm_old_gc_time | JVM Old GC耗时 | 该指标用于统计测量对象的JVM Old GC耗时累计值。 | ≥ 0 | ms | 不涉及 | cluster_id,instance_id | 1分钟 |
| jvm_old_gc_count | JVM Old GC次数 | 该指标用于统计测量对象的JVM Old GC次数累计值。 | ≥ 0 | Count | 不涉及 | cluster_id,instance_id | 1分钟 |
| disk_iops_qos_num | 磁盘IOPS超限次数 | 所有磁盘IOPS超限次数的总和。 | ≥ 0 | Count | 不涉及 | cluster_id,instance_id | 1分钟 |
| disk_iobw_qos_num | 磁盘IO带宽超限次数 | 所有磁盘IO带宽超限次数的总和。 | ≥ 0 | Count | 不涉及 | cluster_id,instance_id | 1分钟 |
| max_disk_io_util | 最大磁盘IO使用率 | 所有磁盘IO使用率中的最大值。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |
| avg_disk_io_util | 平均磁盘IO使用率 | 所有磁盘IO使用率的平均值。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |
| shard_quota_usage | 分片数配额使用率 | 当前配置的分片数与分片数上限值之比。 | 0~100 | % | 不涉及 | cluster_id,instance_id | 1分钟 |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| cluster_id | 集群ID | 该值可通过CSS服务的查询集群列表接口获取，位于响应体的clusters[].id字段，即集群ID。 |
| cluster_id,instance_id | 集群节点ID | 该值可通过CSS服务的查询集群列表接口获取，位于响应体的clusters[].instances[].id字段，即集群实例ID。 |

## 使用说明

1. 命名空间: SYS.ES
2. 监控周期: 1分钟（原始指标）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询CSS服务中Elasticsearch集群节点的CPU利用率（cpu_usage），该指标的维度信息为"cluster_id,instance_id"，表示cluster_id为0层，instance_id为1层
   - 通过API查询单个监控指标时: dim.0=cluster_id,{cluster_id值}&dim.1=instance_id,{instance_id值}
   - 通过API批量查询监控指标时: "dimensions": [{"name": "cluster_id", "value": "{cluster_id值}"}, {"name": "instance_id", "value": "{instance_id值}"}]
5. 累计值说明: 部分指标为累计值，从节点启动时开始叠加数值，当节点重启后清零重新累计