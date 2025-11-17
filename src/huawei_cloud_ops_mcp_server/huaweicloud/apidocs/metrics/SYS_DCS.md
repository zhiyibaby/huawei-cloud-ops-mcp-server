SYS.DCS (分布式缓存服务监控指标) 监控指标文档:

命名空间: SYS.DCS

说明: DCS服务上报云监控服务的监控指标，用于监控分布式缓存服务实例的性能指标。监控周期为1分钟。云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级。

## 实例监控指标差异说明

| 实例类型 | 实例级监控 | 数据节点级监控 | Proxy节点级监控 |
|---------|----------|--------------|---------------|
| 单机 | 支持 只有实例级别的监控指标，实例监控即为数据节点监控 | 不涉及 | 不涉及 |
| 主备 | 支持 实例监控是指对主节点的监控 | 支持 数据节点监控分别是对主节点和备节点的监控 | 不涉及 |
| 读写分离 | 支持 实例监控是指对主节点的监控 | 支持 数据节点监控分别是对主节点和备节点的监控 | 支持 Proxy节点监控是对实例中每个Proxy节点的监控 |
| Proxy集群 | 支持 实例监控是对集群所有主节点数据汇总后的监控 | 支持 数据节点监控是对集群每个分片的监控 | 支持 Proxy节点监控是对集群每个Proxy节点的监控 |
| Cluster集群 | 支持 实例监控是对集群所有主节点数据汇总后的监控 | 支持 数据节点监控是对集群每个分片的监控 | 不涉及 |

## Redis 3.0实例监控指标

注意: DCS Redis 3.0已下线，暂停售卖，建议使用Redis 5.0及以上版本。

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。如果是单机/主备实例，该指标为主节点的CPU值。如果是Proxy集群实例，该指标为各个Proxy节点的平均值。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_hits | 缓存命中次数 | 该指标用于统计测量对象缓存命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_misses | 缓存未命中次数 | 该指标用于统计测量对象缓存未命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| used_memory | 已用内存 | 该指标用于统计测量对象已用内存。 | ≥ 0 | Byte | 1024(IEC) | dcs_instance_id | 1分钟 |
| evicted_keys | 已逐出的键数量 | 该指标用于统计测量对象已逐出的键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_instance_id | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| keys | 键总数 | 该指标用于统计测量对象键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| expires | 过期键总数 | 该指标用于统计测量对象过期键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_channels | 发布订阅频道数 | 该指标用于统计测量对象发布订阅频道数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_patterns | 发布订阅模式数 | 该指标用于统计测量对象发布订阅模式数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| blocked_clients | 阻塞客户端数 | 该指标用于统计测量对象阻塞客户端数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_commands_processed | 命令处理总数 | 该指标用于统计测量对象命令处理总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_connections_received | 连接总数 | 该指标用于统计测量对象连接总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_keys | 键空间键数量 | 该指标用于统计测量对象键空间键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_expires | 键空间过期键数量 | 该指标用于统计测量对象键空间过期键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |

## Redis 4.0/5.0实例监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。如果是单机/主备实例，该指标为主节点的CPU值。如果是Proxy集群实例，该指标为各个Proxy节点的平均值。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_hits | 缓存命中次数 | 该指标用于统计测量对象缓存命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_misses | 缓存未命中次数 | 该指标用于统计测量对象缓存未命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| used_memory | 已用内存 | 该指标用于统计测量对象已用内存。 | ≥ 0 | Byte | 1024(IEC) | dcs_instance_id | 1分钟 |
| evicted_keys | 已逐出的键数量 | 该指标用于统计测量对象已逐出的键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_instance_id | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| keys | 键总数 | 该指标用于统计测量对象键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| expires | 过期键总数 | 该指标用于统计测量对象过期键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_channels | 发布订阅频道数 | 该指标用于统计测量对象发布订阅频道数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_patterns | 发布订阅模式数 | 该指标用于统计测量对象发布订阅模式数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| blocked_clients | 阻塞客户端数 | 该指标用于统计测量对象阻塞客户端数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_commands_processed | 命令处理总数 | 该指标用于统计测量对象命令处理总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_connections_received | 连接总数 | 该指标用于统计测量对象连接总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_keys | 键空间键数量 | 该指标用于统计测量对象键空间键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_expires | 键空间过期键数量 | 该指标用于统计测量对象键空间过期键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |

## Redis 6.0实例监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。如果是单机/主备实例，该指标为主节点的CPU值。如果是Proxy集群实例，该指标为各个Proxy节点的平均值。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_instance_id | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_hits | 缓存命中次数 | 该指标用于统计测量对象缓存命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_misses | 缓存未命中次数 | 该指标用于统计测量对象缓存未命中次数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| used_memory | 已用内存 | 该指标用于统计测量对象已用内存。 | ≥ 0 | Byte | 1024(IEC) | dcs_instance_id | 1分钟 |
| evicted_keys | 已逐出的键数量 | 该指标用于统计测量对象已逐出的键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_instance_id | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id | 1分钟 |
| keys | 键总数 | 该指标用于统计测量对象键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| expires | 过期键总数 | 该指标用于统计测量对象过期键总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_channels | 发布订阅频道数 | 该指标用于统计测量对象发布订阅频道数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| pubsub_patterns | 发布订阅模式数 | 该指标用于统计测量对象发布订阅模式数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| blocked_clients | 阻塞客户端数 | 该指标用于统计测量对象阻塞客户端数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_commands_processed | 命令处理总数 | 该指标用于统计测量对象命令处理总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| total_connections_received | 连接总数 | 该指标用于统计测量对象连接总数。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_keys | 键空间键数量 | 该指标用于统计测量对象键空间键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |
| keyspace_expires | 键空间过期键数量 | 该指标用于统计测量对象键空间过期键数量。 | ≥ 0 | count | dcs_instance_id | 1分钟 |

## Memcached实例监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。 | 0～100 | % | 不涉及 | dcs_memcached_instance_id | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_memcached_instance_id | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_memcached_instance_id | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_memcached_instance_id | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| keyspace_hits | 缓存命中次数 | 该指标用于统计测量对象缓存命中次数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| keyspace_misses | 缓存未命中次数 | 该指标用于统计测量对象缓存未命中次数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| used_memory | 已用内存 | 该指标用于统计测量对象已用内存。 | ≥ 0 | Byte | 1024(IEC) | dcs_memcached_instance_id | 1分钟 |
| evicted_keys | 已逐出的键数量 | 该指标用于统计测量对象已逐出的键数量。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_memcached_instance_id | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_memcached_instance_id | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_memcached_instance_id | 1分钟 |
| keys | 键总数 | 该指标用于统计测量对象键总数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| expires | 过期键总数 | 该指标用于统计测量对象过期键总数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| total_commands_processed | 命令处理总数 | 该指标用于统计测量对象命令处理总数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |
| total_connections_received | 连接总数 | 该指标用于统计测量对象连接总数。 | ≥ 0 | count | dcs_memcached_instance_id | 1分钟 |

## 数据节点级监控指标

数据节点级监控指标适用于主备、读写分离、Proxy集群和Cluster集群实例。指标ID与实例级监控指标相同，但维度包含 dcs_instance_id 和 dcs_cluster_redis_node。

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。 | 0～100 | % | 不涉及 | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| keyspace_hits | 缓存命中次数 | 该指标用于统计测量对象缓存命中次数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| keyspace_misses | 缓存未命中次数 | 该指标用于统计测量对象缓存未命中次数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| used_memory | 已用内存 | 该指标用于统计测量对象已用内存。 | ≥ 0 | Byte | 1024(IEC) | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| evicted_keys | 已逐出的键数量 | 该指标用于统计测量对象已逐出的键数量。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| keys | 键总数 | 该指标用于统计测量对象键总数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| expires | 过期键总数 | 该指标用于统计测量对象过期键总数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| pubsub_channels | 发布订阅频道数 | 该指标用于统计测量对象发布订阅频道数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| pubsub_patterns | 发布订阅模式数 | 该指标用于统计测量对象发布订阅模式数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| blocked_clients | 阻塞客户端数 | 该指标用于统计测量对象阻塞客户端数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| total_commands_processed | 命令处理总数 | 该指标用于统计测量对象命令处理总数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| total_connections_received | 连接总数 | 该指标用于统计测量对象连接总数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| keyspace_keys | 键空间键数量 | 该指标用于统计测量对象键空间键数量。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |
| keyspace_expires | 键空间过期键数量 | 该指标用于统计测量对象键空间过期键数量。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_redis_node | 1分钟 |

## Proxy节点级监控指标

Proxy节点级监控指标适用于读写分离和Proxy集群实例。指标ID与实例级监控指标相同，但维度包含 dcs_instance_id 和 dcs_cluster_proxy2_node（Redis 4.0及以上版本）或 dcs_cluster_proxy_node（Redis 3.0）。

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| cpu_usage | 最大CPU使用率 | 该指标对于统计周期内的测量对象的CPU使用率进行多次采样，表示多次采样的最高值。 | 0～100 | % | 不涉及 | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| memory_usage | 内存利用率 | 该指标用于统计测量对象的内存利用率（内存利用率统计是扣除预留内存的）。 | 0～100 | % | 不涉及 | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| net_in_throughput | 网络输入吞吐量 | 该指标用于统计网口平均每秒的输入流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| net_out_throughput | 网络输出吞吐量 | 该指标用于统计网口平均每秒的输出流量。 | ≥ 0 | byte/s | 1024(IEC) | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| connected_clients | 活跃连接数 | 该指标用于统计测量对象当前活跃连接数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| rejected_connections | 已拒绝的连接数 | 该指标用于统计测量对象已拒绝的连接数。 | ≥ 0 | count | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| instantaneous_ops_per_sec | 每秒操作数 | 该指标用于统计测量对象每秒操作数。 | ≥ 0 | ops/s | 不涉及 | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| instantaneous_input_kbps | 瞬时输入流量 | 该指标用于统计测量对象瞬时输入流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |
| instantaneous_output_kbps | 瞬时输出流量 | 该指标用于统计测量对象瞬时输出流量。 | ≥ 0 | kbit/s | 1024(IEC) | dcs_instance_id,dcs_cluster_proxy2_node | 1分钟 |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| dcs_instance_id | Redis实例ID | 调用查询所有实例列表API，从接口返回的响应参数instance_id中提取。例如：ca3c18f7-xxxx-xxxx-xxxx-76140724f2e4 |
| dcs_cluster_redis_node | 数据节点ID | 调用查询实例节点信息API，从接口返回的响应参数logical_node_id中提取。例如：b6258192xxxxxxxxx380a60c01f6 |
| dcs_cluster_proxy_node | Redis 3.0 Proxy节点ID | Redis 3.0实例已停售，如需获取该取值，请联系客服。例如：a95f06b5xxxxxxee209a8a5ba |
| dcs_cluster_proxy2_node | Redis 4.0及以上版本Proxy节点ID | 调用查询实例节点信息API，从接口返回的响应参数logical_node_id中提取。例如：ff8080819axxxxxxxxb97ba16ae4 |
| dcs_memcached_instance_id | Memcached实例ID | 调用查询所有实例列表API，从接口返回的响应参数instance_id中提取。例如：f987f2d6-xxxx-xxxx-xxxx-e3c49341f014 |

## 使用说明

1. 命名空间: SYS.DCS
2. 监控周期: 1分钟（原始指标）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询数据节点的CPU使用率（cpu_usage），维度信息为"dcs_instance_id,dcs_cluster_redis_node"，表示dcs_instance_id为0层，dcs_cluster_redis_node为1层
   - API查询时: dim.0=dcs_instance_id,{dcs_instance_id值}&dim.1=dcs_cluster_redis_node,{dcs_cluster_redis_node值}
5. 进制说明: net_in_throughput、net_out_throughput、used_memory、instantaneous_input_kbps、instantaneous_output_kbps 使用 1024(IEC) 进制
6. 实例类型差异: 不同实例类型支持的监控层级不同，请参考"实例监控指标差异说明"表格

