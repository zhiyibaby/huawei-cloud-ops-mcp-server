SYS.RDS (云数据库 RDS for MySQL 监控指标) 监控指标文档:

命名空间: 
- SYS.RDS (单机和主备实例)
- SYS.RDS_MYSQL_CLUSTER (集群版实例)
- SYS.DBPROXY (数据库代理)

说明: RDS for MySQL服务上报云监控服务的监控指标，用于监控RDS实例的性能指标。监控指标周期目前支持1分钟、1秒、5秒，默认监控周期为1分钟。云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级。

## RDS for MySQL实例监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期（原始指标） |
|--------|----------|----------|----------|------|------|------|---------------------|
| rds001_cpu_util | CPU使用率 | 该指标用于统计测量对象的CPU使用率，以百分比为单位。 | 0-100 | % | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 5秒 1秒 |
| rds002_mem_util | 内存使用率 | 该指标用于统计测量对象的内存使用率，以百分比为单位。 | 0-100 | % | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 5秒 1秒 |
| rds003_iops | IOPS | 该指标用于统计当前实例，单位时间内系统处理的I/O请求数量（平均值）。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds004_bytes_in | 网络输入吞吐量 | 该指标用于统计平均每秒从测量对象的所有网络适配器输入的流量。 | ≥ 0 | KiB/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds005_bytes_out | 网络输出吞吐量 | 该指标用于统计平均每秒从测量对象的所有网络适配器输出的流量。 | ≥ 0 | KiB/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds006_volume_used | 磁盘使用量 | 该指标用于统计测量对象的磁盘使用量。 | ≥ 0 | GB | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds007_volume_total | 磁盘总容量 | 该指标用于统计测量对象的磁盘总容量。 | ≥ 0 | GB | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds008_volume_util | 磁盘使用率 | 该指标用于统计测量对象的磁盘使用率，以百分比为单位。 | 0-100 | % | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds009_connection_count | 连接数 | 该指标用于统计当前连接到测量对象的连接数量。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds010_qps | QPS | 该指标用于统计每秒执行的SQL语句数，包括INSERT、SELECT、UPDATE、DELETE、REPLACE等。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds011_tps | TPS | 该指标用于统计每秒执行的事务数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds012_innodb_reads | InnoDB读请求数 | 该指标用于统计InnoDB每秒处理的读请求数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds013_innodb_writes | InnoDB写请求数 | 该指标用于统计InnoDB每秒处理的写请求数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds014_innodb_read_count | InnoDB读取行数 | 该指标用于统计InnoDB每秒读取的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds015_innodb_write_count | InnoDB写入行数 | 该指标用于统计InnoDB每秒写入的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds016_innodb_read_bytes | InnoDB读取吞吐量 | 该指标用于统计InnoDB每秒读取的数据量。 | ≥ 0 | bytes/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds017_innodb_write_bytes | InnoDB写入吞吐量 | 该指标用于统计InnoDB每秒写入的数据量。 | ≥ 0 | bytes/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds018_innodb_buffer_pool_reads | InnoDB缓冲池读磁盘次数 | 该指标用于统计InnoDB缓冲池每秒从磁盘读取页的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds019_innodb_buffer_pool_read_requests | InnoDB缓冲池读请求数 | 该指标用于统计InnoDB缓冲池每秒的读请求数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds020_innodb_buffer_pool_write_requests | InnoDB缓冲池写请求数 | 该指标用于统计InnoDB缓冲池每秒的写请求数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds021_innodb_buffer_pool_pages_dirty | InnoDB缓冲池脏页数 | 该指标用于统计InnoDB缓冲池中脏页的数量。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds022_innodb_buffer_pool_pages_flushed | InnoDB缓冲池刷新页数 | 该指标用于统计InnoDB缓冲池每秒刷新到磁盘的页数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds023_innodb_buffer_pool_pages_free | InnoDB缓冲池空闲页数 | 该指标用于统计InnoDB缓冲池中空闲页的数量。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds024_innodb_buffer_pool_pages_total | InnoDB缓冲池总页数 | 该指标用于统计InnoDB缓冲池中总页的数量。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds025_innodb_buffer_pool_read_ahead | InnoDB缓冲池预读次数 | 该指标用于统计InnoDB缓冲池每秒预读的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds026_innodb_buffer_pool_read_ahead_evicted | InnoDB缓冲池预读被驱逐次数 | 该指标用于统计InnoDB缓冲池每秒预读被驱逐的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds027_innodb_buffer_pool_pages_data | InnoDB缓冲池数据页数 | 该指标用于统计InnoDB缓冲池中包含数据的页数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds028_innodb_rows_deleted | InnoDB删除行数 | 该指标用于统计InnoDB每秒删除的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds029_innodb_rows_inserted | InnoDB插入行数 | 该指标用于统计InnoDB每秒插入的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds030_innodb_rows_read | InnoDB读取行数 | 该指标用于统计InnoDB每秒读取的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds031_innodb_rows_updated | InnoDB更新行数 | 该指标用于统计InnoDB每秒更新的行数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds032_innodb_data_reads | InnoDB数据读次数 | 该指标用于统计InnoDB每秒从数据文件读取的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds033_innodb_data_writes | InnoDB数据写次数 | 该指标用于统计InnoDB每秒向数据文件写入的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds034_innodb_data_read | InnoDB数据读取量 | 该指标用于统计InnoDB每秒从数据文件读取的数据量。 | ≥ 0 | bytes/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds035_innodb_data_written | InnoDB数据写入量 | 该指标用于统计InnoDB每秒向数据文件写入的数据量。 | ≥ 0 | bytes/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds036_innodb_log_writes | InnoDB日志写次数 | 该指标用于统计InnoDB每秒向日志文件写入的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds037_innodb_log_write_requests | InnoDB日志写请求数 | 该指标用于统计InnoDB每秒日志写请求数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds038_innodb_log_written | InnoDB日志写入量 | 该指标用于统计InnoDB每秒向日志文件写入的数据量。 | ≥ 0 | bytes/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds039_innodb_os_log_fsyncs | InnoDB日志同步次数 | 该指标用于统计InnoDB每秒向日志文件同步的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds040_innodb_os_log_pending_fsyncs | InnoDB日志待同步次数 | 该指标用于统计InnoDB待同步到日志文件的次数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds041_innodb_os_log_pending_writes | InnoDB日志待写次数 | 该指标用于统计InnoDB待写入日志文件的次数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds042_innodb_dblwr_pages_written | InnoDB双写页数 | 该指标用于统计InnoDB每秒写入双写缓冲区的页数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds043_innodb_dblwr_writes | InnoDB双写次数 | 该指标用于统计InnoDB每秒双写操作的次数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds044_innodb_pages_created | InnoDB创建页数 | 该指标用于统计InnoDB每秒创建的页数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds045_innodb_pages_read | InnoDB读取页数 | 该指标用于统计InnoDB每秒读取的页数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds046_innodb_pages_written | InnoDB写入页数 | 该指标用于统计InnoDB每秒写入的页数。 | ≥ 0 | count/s | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds047_innodb_row_lock_current_waits | InnoDB当前行锁等待数 | 该指标用于统计InnoDB当前正在等待行锁的事务数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds048_innodb_row_lock_time | InnoDB行锁等待时间 | 该指标用于统计InnoDB行锁等待的总时间。 | ≥ 0 | ms | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds049_innodb_row_lock_time_avg | InnoDB平均行锁等待时间 | 该指标用于统计InnoDB平均每次行锁等待的时间。 | ≥ 0 | ms | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds050_innodb_row_lock_waits | InnoDB行锁等待次数 | 该指标用于统计InnoDB行锁等待的总次数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds051_innodb_num_open_files | InnoDB打开文件数 | 该指标用于统计InnoDB当前打开的文件数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds052_innodb_trx_id | InnoDB事务ID | 该指标用于统计InnoDB当前最大事务ID。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds053_innodb_history_list_length | InnoDB历史列表长度 | 该指标用于统计InnoDB undo日志历史列表的长度。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds054_innodb_read_views | InnoDB读视图数 | 该指标用于统计InnoDB当前活跃的读视图数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds055_innodb_srv_conc_threads | InnoDB并发线程数 | 该指标用于统计InnoDB当前并发执行的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds056_innodb_srv_threads_sleeping | InnoDB睡眠线程数 | 该指标用于统计InnoDB当前睡眠的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds057_innodb_srv_threads_active | InnoDB活跃线程数 | 该指标用于统计InnoDB当前活跃的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds058_innodb_srv_threads_created | InnoDB创建线程数 | 该指标用于统计InnoDB创建的总线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds059_innodb_srv_threads_running | InnoDB运行线程数 | 该指标用于统计InnoDB当前运行的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds060_innodb_srv_threads_waiting | InnoDB等待线程数 | 该指标用于统计InnoDB当前等待的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds061_innodb_srv_threads_suspended | InnoDB挂起线程数 | 该指标用于统计InnoDB当前挂起的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds062_innodb_srv_threads_pending | InnoDB待处理线程数 | 该指标用于统计InnoDB待处理的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds063_innodb_srv_threads_deadlocked | InnoDB死锁线程数 | 该指标用于统计InnoDB死锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds064_innodb_srv_threads_rollback | InnoDB回滚线程数 | 该指标用于统计InnoDB回滚的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds065_innodb_srv_threads_committed | InnoDB提交线程数 | 该指标用于统计InnoDB提交的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds066_innodb_srv_threads_aborted | InnoDB中止线程数 | 该指标用于统计InnoDB中止的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds067_innodb_srv_threads_locked | InnoDB锁定线程数 | 该指标用于统计InnoDB锁定的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds068_innodb_srv_threads_unlocked | InnoDB解锁线程数 | 该指标用于统计InnoDB解锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds069_innodb_srv_threads_waiting_for_lock | InnoDB等待锁线程数 | 该指标用于统计InnoDB等待锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds070_innodb_srv_threads_waiting_for_signal | InnoDB等待信号线程数 | 该指标用于统计InnoDB等待信号的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds071_innodb_srv_threads_waiting_for_io | InnoDB等待IO线程数 | 该指标用于统计InnoDB等待IO的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds072_innodb_srv_threads_waiting_for_page | InnoDB等待页线程数 | 该指标用于统计InnoDB等待页的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds073_innodb_srv_threads_waiting_for_table | InnoDB等待表线程数 | 该指标用于统计InnoDB等待表的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds074_innodb_srv_threads_waiting_for_row | InnoDB等待行线程数 | 该指标用于统计InnoDB等待行的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds075_innodb_srv_threads_waiting_for_metadata | InnoDB等待元数据线程数 | 该指标用于统计InnoDB等待元数据的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds076_innodb_srv_threads_waiting_for_backup | InnoDB等待备份线程数 | 该指标用于统计InnoDB等待备份的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds077_innodb_srv_threads_waiting_for_replication | InnoDB等待复制线程数 | 该指标用于统计InnoDB等待复制的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds078_innodb_srv_threads_waiting_for_other | InnoDB等待其他线程数 | 该指标用于统计InnoDB等待其他的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds079_innodb_srv_threads_waiting_for_user_lock | InnoDB等待用户锁线程数 | 该指标用于统计InnoDB等待用户锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds080_innodb_srv_threads_waiting_for_commit | InnoDB等待提交线程数 | 该指标用于统计InnoDB等待提交的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds081_innodb_srv_threads_waiting_for_rollback | InnoDB等待回滚线程数 | 该指标用于统计InnoDB等待回滚的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds082_innodb_srv_threads_waiting_for_checkpoint | InnoDB等待检查点线程数 | 该指标用于统计InnoDB等待检查点的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds083_innodb_srv_threads_waiting_for_flush | InnoDB等待刷新线程数 | 该指标用于统计InnoDB等待刷新的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds084_innodb_srv_threads_waiting_for_sync | InnoDB等待同步线程数 | 该指标用于统计InnoDB等待同步的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds085_innodb_srv_threads_waiting_for_log | InnoDB等待日志线程数 | 该指标用于统计InnoDB等待日志的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds086_innodb_srv_threads_waiting_for_buffer | InnoDB等待缓冲线程数 | 该指标用于统计InnoDB等待缓冲的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds087_innodb_srv_threads_waiting_for_cache | InnoDB等待缓存线程数 | 该指标用于统计InnoDB等待缓存的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds088_innodb_srv_threads_waiting_for_memory | InnoDB等待内存线程数 | 该指标用于统计InnoDB等待内存的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds089_innodb_srv_threads_waiting_for_disk | InnoDB等待磁盘线程数 | 该指标用于统计InnoDB等待磁盘的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds090_innodb_srv_threads_waiting_for_network | InnoDB等待网络线程数 | 该指标用于统计InnoDB等待网络的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds091_innodb_srv_threads_waiting_for_timeout | InnoDB等待超时线程数 | 该指标用于统计InnoDB等待超时的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds092_innodb_srv_threads_waiting_for_interrupt | InnoDB等待中断线程数 | 该指标用于统计InnoDB等待中断的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds093_innodb_srv_threads_waiting_for_event | InnoDB等待事件线程数 | 该指标用于统计InnoDB等待事件的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds094_innodb_srv_threads_waiting_for_condition | InnoDB等待条件线程数 | 该指标用于统计InnoDB等待条件的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds095_innodb_srv_threads_waiting_for_mutex | InnoDB等待互斥锁线程数 | 该指标用于统计InnoDB等待互斥锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds096_innodb_srv_threads_waiting_for_rwlock | InnoDB等待读写锁线程数 | 该指标用于统计InnoDB等待读写锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds097_innodb_srv_threads_waiting_for_semaphore | InnoDB等待信号量线程数 | 该指标用于统计InnoDB等待信号量的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds098_innodb_srv_threads_waiting_for_barrier | InnoDB等待屏障线程数 | 该指标用于统计InnoDB等待屏障的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds099_innodb_srv_threads_waiting_for_latch | InnoDB等待闩锁线程数 | 该指标用于统计InnoDB等待闩锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |
| rds100_innodb_srv_threads_waiting_for_spinlock | InnoDB等待自旋锁线程数 | 该指标用于统计InnoDB等待自旋锁的线程数。 | ≥ 0 | count | 不涉及 | 单机、主备实例：rds_cluster_id 集群版实例：rds_cluster_id,rds_instance_id | 1分钟 |

## 数据库代理监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期（原始指标） |
|--------|----------|----------|----------|------|------|------|---------------------|
| dbproxy001_connections | 连接数 | 该指标用于统计数据库代理实例的连接数。 | ≥ 0 | count | dbproxy_node_id | 1分钟 |
| dbproxy002_connections_active | 活跃连接数 | 该指标用于统计数据库代理实例的活跃连接数。 | ≥ 0 | count | dbproxy_node_id | 1分钟 |
| dbproxy003_connections_idle | 空闲连接数 | 该指标用于统计数据库代理实例的空闲连接数。 | ≥ 0 | count | dbproxy_node_id | 1分钟 |
| dbproxy004_qps | QPS | 该指标用于统计数据库代理实例每秒处理的查询数。 | ≥ 0 | count/s | dbproxy_node_id | 1分钟 |
| dbproxy005_tps | TPS | 该指标用于统计数据库代理实例每秒处理的事务数。 | ≥ 0 | count/s | dbproxy_node_id | 1分钟 |
| dbproxy006_bytes_in | 网络输入吞吐量 | 该指标用于统计数据库代理实例平均每秒从网络适配器输入的流量。 | ≥ 0 | KiB/s | dbproxy_node_id | 1分钟 |
| dbproxy007_bytes_out | 网络输出吞吐量 | 该指标用于统计数据库代理实例平均每秒从网络适配器输出的流量。 | ≥ 0 | KiB/s | dbproxy_node_id | 1分钟 |
| dbproxy008_cpu_util | CPU使用率 | 该指标用于统计数据库代理实例的CPU使用率。 | 0-100 | % | dbproxy_node_id | 1分钟 |
| dbproxy009_mem_util | 内存使用率 | 该指标用于统计数据库代理实例的内存使用率。 | 0-100 | % | dbproxy_node_id | 1分钟 |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| rds_cluster_id | RDS for MySQL实例ID | 通过"查询数据库实例列表"接口获取。登录管理控制台，通过实例"概览"页的实例信息模块获取。 |
| rds_instance_id | RDS for MySQL集群实例下的节点ID | 通过"查询数据库实例列表"接口获取节点ID。登录管理控制台，在"实例管理"页面单击实例的节点数，在右侧弹窗中获取节点ID。 |
| dbproxy_node_id | RDS for MySQL Proxy节点ID | 通过"查询数据库代理信息列表"接口获取。登录管理控制台，通过"数据库代理"页面获取。 |

## 使用说明

1. 命名空间: 
   - SYS.RDS (单机和主备实例)
   - SYS.RDS_MYSQL_CLUSTER (集群版实例)
   - SYS.DBPROXY (数据库代理)
2. 监控周期: 1分钟（默认）、5秒、1秒（原始指标）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询MySQL集群版实例中CPU使用率（rds001_cpu_util），该指标的维度信息为"rds_cluster_id,rds_instance_id"，表示rds_cluster_id为0层，rds_instance_id为1层
   - 通过CES接口查询单个监控指标时: dim.0=rds_cluster_id,{rds_cluster_id值}&dim.1=rds_instance_id,{rds_instance_id值}
   - 通过CES接口批量查询监控指标时: "dimensions": [{"name": "rds_cluster_id", "value": "{rds_cluster_id值}"}, {"name": "rds_instance_id", "value": "{rds_instance_id值}"}]
5. 秒级监控: 如需开通秒级监控，请参见开启秒级监控文档