SYS.EVS (云硬盘基础监控指标) 监控指标文档:

命名空间: SYS.EVS

说明: 云硬盘服务上报云监控服务的监控指标，用于监控云硬盘的带宽、IOPS等性能指标。监控周期为5分钟。

## 云硬盘监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|----------|
| disk_device_read_bytes_rate | 云硬盘读带宽 | 该指标用于统计每秒从测量对象读出的数据量。 | ≥ 0 | bytes/s | disk_name | 5分钟(采点瞬时值) |
| disk_device_write_bytes_rate | 云硬盘写带宽 | 该指标用于统计每秒写入测量对象的数据量。 | ≥ 0 | bytes/s | disk_name | 5分钟(采点瞬时值) |
| disk_device_read_requests_rate | 云硬盘读IOPS | 该指标用于统计每秒从测量对象读取数据的请求次数。 | ≥ 0 | requests/s | disk_name | 5分钟(采点瞬时值) |
| disk_device_write_requests_rate | 云硬盘写IOPS | 该指标用于统计每秒到测量对象写入数据的请求次数。 | ≥ 0 | requests/s | disk_name | 5分钟(采点瞬时值) |
| disk_device_queue_length | 平均队列长度 | 该指标用于统计测量对象在测量周期内平均等待完成的读取或写入操作请求的数量。 | ≥ 0 | count | disk_name | 5分钟(采点瞬时值) |
| disk_device_io_util | 云硬盘读写使用率 | 该指标用于统计测量对象在测量周期内提交读取或写入操作的占比。 | 0-100 | % | disk_name | 5分钟(采点瞬时值) |
| disk_device_write_bytes_per_operation | 平均写操作大小 | 该指标用于统计测量对象在测量周期内平均每个写IO操作传输的字节数。 | ≥ 0 | KB/op | disk_name | 5分钟(采点瞬时值) |
| disk_device_read_bytes_per_operation | 平均读操作大小 | 该指标用于统计测量对象在测量周期内平均每个读IO操作传输的字节数。 | ≥ 0 | KB/op | disk_name | 5分钟(采点瞬时值) |
| disk_device_write_await | 平均写操作耗时 | 该指标用于统计测量对象在测量周期内平均每个写IO的操作时长。 | ≥ 0 | ms/op | disk_name | 5分钟(采点瞬时值) |
| disk_device_read_await | 平均读操作耗时 | 该指标用于统计测量对象在测量周期内平均每个读IO的操作时长。 | ≥ 0 | ms/op | disk_name | 5分钟(采点瞬时值) |
| disk_device_io_svctm | 平均IO服务时长 | 该指标用于统计测量对象在测量周期内平均每个读IO或写IO的服务时长。 | ≥ 0 | ms/op | disk_name | 5分钟(采点瞬时值) |
| disk_device_io_iops_qos_num | IOPS达到上限(次数) | 该指标用于统计测量对象的IOPS达到上限的次数。 | ≥ 0 | count | disk_name | 5分钟(累加值) |
| disk_device_io_iobw_qos_num | 带宽达到上限(次数) | 该指标用于统计测量对象带宽达到上限的次数。 | ≥ 0 | count | disk_name | 5分钟(累加值) |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| disk_name | 云硬盘标识 | 格式为：云服务器实例ID-盘符名（例如：6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d-vda）或 云服务器实例ID-volume-卷ID（例如：6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d-volume-31f45764-38b3-44ad-aaca-4015c83371e6）或 卷ID。云服务器实例ID和盘符名可通过ECS服务的查询弹性云服务器单个磁盘信息获取。卷ID可通过EVS服务的查询单个云硬盘详情获取。 |

## 使用说明

1. 命名空间: SYS.EVS
2. 监控周期: 5分钟（原始指标）
3. 当检测到云硬盘的带宽、IOPS等指标数据较高或者超过限制，建议更换为性能更高的云硬盘类型
4. 进制说明: disk_device_read_bytes_rate 和 disk_device_write_bytes_rate 使用 1024(IEC) 进制