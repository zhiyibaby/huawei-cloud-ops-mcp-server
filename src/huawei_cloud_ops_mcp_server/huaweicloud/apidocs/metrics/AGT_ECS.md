AGT.ECS (弹性云服务器操作系统监控指标 - 安装Agent) 监控指标文档:

命名空间: AGT.ECS

说明: 通过在弹性云服务器中安装Agent插件，为用户提供服务器的系统级、主动式、细颗粒度监控服务。指标采集周期是1分钟。

## CPU相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| cpu_usage | (Agent) CPU使用率 | 该指标用于统计测量对象当前CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。采集方式（Windows）：通过WindowsAPI GetSystemTimes获取。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_idle | (Agent) CPU空闲时间占比 | 该指标用于统计测量对象当前CPU空闲时间占比。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出CPU空闲时间占比。采集方式（Windows）：通过WindowsAPI GetSystemTimes获取。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_user | (Agent) 用户空间CPU使用率 | 该指标用于统计测量对象当前用户空间占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。采集方式（Windows）：通过WindowsAPI GetSystemTimes获取。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_system | (Agent) 内核空间CPU使用率 | 该指标用于统计测量对象当前内核空间占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。采集方式（Windows）：通过WindowsAPI GetSystemTimes获取。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_iowait | (Agent) IO等待占用CPU使用率 | 该指标用于统计测量对象当前IO等待占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_other | (Agent) 其他占用CPU使用率 | 该指标用于统计测量对象当前其他占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。采集方式（Windows）：通过WindowsAPI GetSystemTimes获取。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_guest | (Agent) 客户占用CPU使用率 | 该指标用于统计测量对象当前客户占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_nice | (Agent) 低优先级用户空间CPU使用率 | 该指标用于统计测量对象当前低优先级用户空间占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_irq | (Agent) 硬中断占用CPU使用率 | 该指标用于统计测量对象当前硬中断占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_softirq | (Agent) 软中断占用CPU使用率 | 该指标用于统计测量对象当前软中断占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |
| cpu_usage_steal | (Agent) 虚拟化环境下其他租户占用CPU使用率 | 该指标用于统计测量对象当前虚拟化环境下其他租户占用CPU使用率。采集方式（Linux）：通过计算采集周期内/proc/stat中的变化得出cpu使用率。 | 0-100 | % | instance_id | 1分钟 |

## CPU负载类相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| load1 | (Agent) 1分钟平均负载 | 该指标用于统计测量对象过去1分钟的CPU平均负载。采集方式（Linux）：通过/proc/loadavg获取。 | >= 0 | - | instance_id | 1分钟 |
| load5 | (Agent) 5分钟平均负载 | 该指标用于统计测量对象过去5分钟的CPU平均负载。采集方式（Linux）：通过/proc/loadavg获取。 | >= 0 | - | instance_id | 1分钟 |
| load15 | (Agent) 15分钟平均负载 | 该指标用于统计测量对象过去15分钟的CPU平均负载。采集方式（Linux）：通过/proc/loadavg获取。 | >= 0 | - | instance_id | 1分钟 |

## 内存相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| mem_usedPercent | (Agent) 内存使用率 | 该指标用于统计测量对象的内存使用率。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | 0-100 | % | instance_id | 1分钟 |
| mem_total | (Agent) 内存总量 | 该指标用于统计测量对象的内存总量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_used | (Agent) 内存使用量 | 该指标用于统计测量对象的内存使用量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_free | (Agent) 内存空闲量 | 该指标用于统计测量对象的内存空闲量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_available | (Agent) 可用内存 | 该指标用于统计测量对象的可用内存。采集方式（Linux）：通过/proc/meminfo获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_buffers | (Agent) 缓冲内存 | 该指标用于统计测量对象的缓冲内存。采集方式（Linux）：通过/proc/meminfo获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_cached | (Agent) 缓存内存 | 该指标用于统计测量对象的缓存内存。采集方式（Linux）：通过/proc/meminfo获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_swapTotal | (Agent) 交换区总量 | 该指标用于统计测量对象的交换区总量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_swapFree | (Agent) 交换区空闲量 | 该指标用于统计测量对象的交换区空闲量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_swapUsed | (Agent) 交换区使用量 | 该指标用于统计测量对象的交换区使用量。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | >= 0 | MB | instance_id | 1分钟 |
| mem_swapUsedPercent | (Agent) 交换区使用率 | 该指标用于统计测量对象的交换区使用率。采集方式（Linux）：通过/proc/meminfo获取。采集方式（Windows）：通过WindowsAPI GlobalMemoryStatusEx获取。 | 0-100 | % | instance_id | 1分钟 |

## 磁盘相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| disk_total | (Agent) 磁盘总容量 | 该指标用于统计测量对象的磁盘总容量。采集方式（Linux）：通过df命令获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx获取。 | >= 0 | GB | instance_id, mount_point | 1分钟 |
| disk_used | (Agent) 磁盘使用量 | 该指标用于统计测量对象的磁盘使用量。采集方式（Linux）：通过df命令获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx获取。 | >= 0 | GB | instance_id, mount_point | 1分钟 |
| disk_free | (Agent) 磁盘剩余容量 | 该指标用于统计测量对象的磁盘剩余容量。采集方式（Linux）：通过df命令获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx获取。 | >= 0 | GB | instance_id, mount_point | 1分钟 |
| disk_usedPercent | (Agent) 磁盘使用率 | 该指标用于统计测量对象的磁盘使用率。采集方式（Linux）：通过df命令获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx获取。 | 0-100 | % | instance_id, mount_point | 1分钟 |
| disk_inodeTotal | (Agent) 磁盘inode总数 | 该指标用于统计测量对象的磁盘inode总数。采集方式（Linux）：通过df命令获取。 | >= 0 | - | instance_id, mount_point | 1分钟 |
| disk_inodeUsed | (Agent) 磁盘inode使用数 | 该指标用于统计测量对象的磁盘inode使用数。采集方式（Linux）：通过df命令获取。 | >= 0 | - | instance_id, mount_point | 1分钟 |
| disk_inodeFree | (Agent) 磁盘inode剩余数 | 该指标用于统计测量对象的磁盘inode剩余数。采集方式（Linux）：通过df命令获取。 | >= 0 | - | instance_id, mount_point | 1分钟 |
| disk_inodeUsedPercent | (Agent) 磁盘inode使用率 | 该指标用于统计测量对象的磁盘inode使用率。采集方式（Linux）：通过df命令获取。 | 0-100 | % | instance_id, mount_point | 1分钟 |

## 磁盘I/O相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| disk_read_bytes_rate | (Agent) 磁盘读速率 | 该指标用于统计测量对象每秒从磁盘读取的字节数。采集方式（Linux）：通过/proc/diskstats获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx和IO性能计数器获取。 | >= 0 | Bytes/s | instance_id, device | 1分钟 |
| disk_write_bytes_rate | (Agent) 磁盘写速率 | 该指标用于统计测量对象每秒向磁盘写入的字节数。采集方式（Linux）：通过/proc/diskstats获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx和IO性能计数器获取。 | >= 0 | Bytes/s | instance_id, device | 1分钟 |
| disk_read_requests_rate | (Agent) 磁盘读IOPS | 该指标用于统计测量对象每秒从磁盘读取的请求次数。采集方式（Linux）：通过/proc/diskstats获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx和IO性能计数器获取。 | >= 0 | Count/s | instance_id, device | 1分钟 |
| disk_write_requests_rate | (Agent) 磁盘写IOPS | 该指标用于统计测量对象每秒向磁盘写入的请求次数。采集方式（Linux）：通过/proc/diskstats获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx和IO性能计数器获取。 | >= 0 | Count/s | instance_id, device | 1分钟 |
| disk_io_await | (Agent) 磁盘IO等待时间 | 该指标用于统计测量对象磁盘IO等待时间。采集方式（Linux）：通过/proc/diskstats获取。 | >= 0 | ms | instance_id, device | 1分钟 |
| disk_io_svctm | (Agent) 磁盘IO服务时间 | 该指标用于统计测量对象磁盘IO服务时间。采集方式（Linux）：通过/proc/diskstats获取。 | >= 0 | ms | instance_id, device | 1分钟 |
| disk_io_util | (Agent) 磁盘IO使用率 | 该指标用于统计测量对象磁盘IO使用率。采集方式（Linux）：通过/proc/diskstats获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx和IO性能计数器获取。 | 0-100 | % | instance_id, device | 1分钟 |

## 文件系统类相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| filesystem_avail | (Agent) 文件系统可用空间 | 该指标用于统计测量对象的文件系统可用空间。采集方式（Linux）：通过statfs系统调用获取。采集方式（Windows）：通过WindowsAPI GetDiskFreeSpaceEx获取。 | >= 0 | GB | instance_id, mount_point | 1分钟 |
| filesystem_files | (Agent) 文件系统文件数 | 该指标用于统计测量对象的文件系统文件数。采集方式（Linux）：通过statfs系统调用获取。 | >= 0 | - | instance_id, mount_point | 1分钟 |
| filesystem_files_free | (Agent) 文件系统空闲文件数 | 该指标用于统计测量对象的文件系统空闲文件数。采集方式（Linux）：通过statfs系统调用获取。 | >= 0 | - | instance_id, mount_point | 1分钟 |
| filesystem_readonly | (Agent) 文件系统是否只读 | 该指标用于统计测量对象的文件系统是否只读。采集方式（Linux）：通过statfs系统调用获取。采集方式（Windows）：通过WindowsAPI GetVolumeInformation获取。 | 0或1 | - | instance_id, mount_point | 1分钟 |

## 网卡类相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| network_incoming_bytes_rate | (Agent) 网卡入速率 | 该指标用于统计测量对象网卡每秒接收的字节数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Bytes/s | instance_id, ethtool | 1分钟 |
| network_outgoing_bytes_rate | (Agent) 网卡出速率 | 该指标用于统计测量对象网卡每秒发送的字节数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Bytes/s | instance_id, ethtool | 1分钟 |
| network_incoming_packets_rate | (Agent) 网卡入包速率 | 该指标用于统计测量对象网卡每秒接收的数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |
| network_outgoing_packets_rate | (Agent) 网卡出包速率 | 该指标用于统计测量对象网卡每秒发送的数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |
| network_incoming_bytes_inband | (Agent) 网卡入流量 | 该指标用于统计测量对象网卡接收的总字节数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Bytes | instance_id, ethtool | 1分钟 |
| network_outgoing_bytes_inband | (Agent) 网卡出流量 | 该指标用于统计测量对象网卡发送的总字节数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Bytes | instance_id, ethtool | 1分钟 |
| network_incoming_packets_inband | (Agent) 网卡入包数 | 该指标用于统计测量对象网卡接收的总数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count | instance_id, ethtool | 1分钟 |
| network_outgoing_packets_inband | (Agent) 网卡出包数 | 该指标用于统计测量对象网卡发送的总数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count | instance_id, ethtool | 1分钟 |
| network_incoming_errors_rate | (Agent) 网卡入错误包速率 | 该指标用于统计测量对象网卡每秒接收的错误数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |
| network_outgoing_errors_rate | (Agent) 网卡出错误包速率 | 该指标用于统计测量对象网卡每秒发送的错误数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |
| network_incoming_dropped_rate | (Agent) 网卡入丢包速率 | 该指标用于统计测量对象网卡每秒接收的丢弃数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |
| network_outgoing_dropped_rate | (Agent) 网卡出丢包速率 | 该指标用于统计测量对象网卡每秒发送的丢弃数据包数。采集方式（Linux）：通过/proc/net/dev获取。采集方式（Windows）：通过WindowsAPI GetIfTable获取。 | >= 0 | Count/s | instance_id, ethtool | 1分钟 |

## NTP类相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| ntp_offset | (Agent) NTP偏移量 | 该指标用于统计测量对象NTP偏移量。采集方式（Linux）：通过ntpdate或chrony命令获取。采集方式（Windows）：通过WindowsAPI获取。 | - | ms | instance_id | 1分钟 |
| ntp_delay | (Agent) NTP延迟 | 该指标用于统计测量对象NTP延迟。采集方式（Linux）：通过ntpdate或chrony命令获取。采集方式（Windows）：通过WindowsAPI获取。 | - | ms | instance_id | 1分钟 |
| ntp_dispersion | (Agent) NTP离散度 | 该指标用于统计测量对象NTP离散度。采集方式（Linux）：通过ntpdate或chrony命令获取。采集方式（Windows）：通过WindowsAPI获取。 | - | ms | instance_id | 1分钟 |
| ntp_jitter | (Agent) NTP抖动 | 该指标用于统计测量对象NTP抖动。采集方式（Linux）：通过ntpdate或chrony命令获取。采集方式（Windows）：通过WindowsAPI获取。 | - | ms | instance_id | 1分钟 |

## TCP连接数类相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| tcp_activeOpens | (Agent) TCP主动连接数 | 该指标用于统计测量对象TCP主动连接数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_passiveOpens | (Agent) TCP被动连接数 | 该指标用于统计测量对象TCP被动连接数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_attemptFails | (Agent) TCP连接失败数 | 该指标用于统计测量对象TCP连接失败数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_currEstab | (Agent) TCP当前连接数 | 该指标用于统计测量对象TCP当前连接数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_inErrs | (Agent) TCP接收错误数 | 该指标用于统计测量对象TCP接收错误数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_outRsts | (Agent) TCP发送重置数 | 该指标用于统计测量对象TCP发送重置数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_retransSegs | (Agent) TCP重传段数 | 该指标用于统计测量对象TCP重传段数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_inSegs | (Agent) TCP接收段数 | 该指标用于统计测量对象TCP接收段数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |
| tcp_outSegs | (Agent) TCP发送段数 | 该指标用于统计测量对象TCP发送段数。采集方式（Linux）：通过/proc/net/sockstat获取。采集方式（Windows）：通过WindowsAPI获取。 | >= 0 | Count | instance_id | 1分钟 |

## GPU相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| gpu_util | (Agent) GPU使用率 | 该指标用于统计测量对象GPU使用率。采集方式（Linux）：通过nvidia-smi命令获取。 | 0-100 | % | instance_id, gpu | 1分钟 |
| gpu_memory_used | (Agent) GPU显存使用量 | 该指标用于统计测量对象GPU显存使用量。采集方式（Linux）：通过nvidia-smi命令获取。 | >= 0 | MB | instance_id, gpu | 1分钟 |
| gpu_memory_total | (Agent) GPU显存总量 | 该指标用于统计测量对象GPU显存总量。采集方式（Linux）：通过nvidia-smi命令获取。 | >= 0 | MB | instance_id, gpu | 1分钟 |
| gpu_memory_util | (Agent) GPU显存使用率 | 该指标用于统计测量对象GPU显存使用率。采集方式（Linux）：通过nvidia-smi命令获取。 | 0-100 | % | instance_id, gpu | 1分钟 |
| gpu_temperature | (Agent) GPU温度 | 该指标用于统计测量对象GPU温度。采集方式（Linux）：通过nvidia-smi命令获取。 | >= 0 | ℃ | instance_id, gpu | 1分钟 |
| gpu_power_used | (Agent) GPU功耗 | 该指标用于统计测量对象GPU功耗。采集方式（Linux）：通过nvidia-smi命令获取。 | >= 0 | W | instance_id, gpu | 1分钟 |

## NPU相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| npu_util | (Agent) NPU使用率 | 该指标用于统计测量对象NPU使用率。采集方式（Linux）：通过NPU监控工具获取。 | 0-100 | % | instance_id, npu | 1分钟 |
| npu_memory_used | (Agent) NPU显存使用量 | 该指标用于统计测量对象NPU显存使用量。采集方式（Linux）：通过NPU监控工具获取。 | >= 0 | MB | instance_id, npu | 1分钟 |
| npu_memory_total | (Agent) NPU显存总量 | 该指标用于统计测量对象NPU显存总量。采集方式（Linux）：通过NPU监控工具获取。 | >= 0 | MB | instance_id, npu | 1分钟 |
| npu_memory_util | (Agent) NPU显存使用率 | 该指标用于统计测量对象NPU显存使用率。采集方式（Linux）：通过NPU监控工具获取。 | 0-100 | % | instance_id, npu | 1分钟 |
| npu_temperature | (Agent) NPU温度 | 该指标用于统计测量对象NPU温度。采集方式（Linux）：通过NPU监控工具获取。 | >= 0 | ℃ | instance_id, npu | 1分钟 |
| npu_power_used | (Agent) NPU功耗 | 该指标用于统计测量对象NPU功耗。采集方式（Linux）：通过NPU监控工具获取。 | >= 0 | W | instance_id, npu | 1分钟 |

## DAVP相关监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| davp_util | (Agent) DAVP使用率 | 该指标用于统计测量对象DAVP使用率。采集方式（Linux）：通过DAVP监控工具获取。 | 0-100 | % | instance_id, davp | 1分钟 |
| davp_memory_used | (Agent) DAVP显存使用量 | 该指标用于统计测量对象DAVP显存使用量。采集方式（Linux）：通过DAVP监控工具获取。 | >= 0 | MB | instance_id, davp | 1分钟 |
| davp_memory_total | (Agent) DAVP显存总量 | 该指标用于统计测量对象DAVP显存总量。采集方式（Linux）：通过DAVP监控工具获取。 | >= 0 | MB | instance_id, davp | 1分钟 |
| davp_memory_util | (Agent) DAVP显存使用率 | 该指标用于统计测量对象DAVP显存使用率。采集方式（Linux）：通过DAVP监控工具获取。 | 0-100 | % | instance_id, davp | 1分钟 |
| davp_temperature | (Agent) DAVP温度 | 该指标用于统计测量对象DAVP温度。采集方式（Linux）：通过DAVP监控工具获取。 | >= 0 | ℃ | instance_id, davp | 1分钟 |
| davp_power_used | (Agent) DAVP功耗 | 该指标用于统计测量对象DAVP功耗。采集方式（Linux）：通过DAVP监控工具获取。 | >= 0 | W | instance_id, davp | 1分钟 |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| instance_id | 云服务器ID | 云服务器的唯一标识符，可通过ECS API获取 |
| mount_point | 云服务器磁盘的挂载点 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |
| device | 云服务器磁盘设备 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |
| ethtool | 云服务器网卡 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |
| gpu | GPU类型云服务器中显卡 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |
| npu | NPU类型云服务器中显卡 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |
| davp | DAVP类型云服务器，其中搭载了DaoCloud DAVP1视频加速卡 | 该取值可通过云监控服务的"查询主机监控维度指标信息"API获取 |

## 使用说明

1. 命名空间: AGT.ECS
2. 监控周期: 1分钟（原始指标）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询磁盘挂载点的剩余存储量（disk_free），维度信息为"instance_id,mount_point"
   - API查询时: dim.0=instance_id,{instance_id值}&dim.1=mount_point,{mount_point值}