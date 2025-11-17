SYS.VPC (虚拟私有云监控指标) 监控指标文档:

命名空间: SYS.VPC

说明: 弹性公网IP和带宽上报云监控的监控指标，用于监控VPC网络的带宽、流量和子网IPv4地址使用情况。监控周期为1分钟（弹性公网IP和带宽）或30分钟（子网IPv4地址）。

## 弹性公网IP和带宽监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| upstream_bandwidth | 出网带宽 | 该指标用于统计测试对象出云平台的网络速度（原指标为上行带宽）。 | ≥ 0 | bit/s | 1000(SI) | bandwidth_id,publicip_id | 1分钟 |
| downstream_bandwidth | 入网带宽 | 该指标用于统计测试对象入云平台的网络速度（原指标为下行带宽）。 | ≥ 0 | bit/s | 1000(SI) | bandwidth_id,publicip_id | 1分钟 |
| upstream_bandwidth_usage | 出网带宽使用率 | 该指标用于统计测量对象出云平台的带宽使用率，以百分比为单位。出网带宽使用率=出网带宽指标/购买的带宽大小 | 0-100 | % | 不涉及 | bandwidth_id,publicip_id | 1分钟 |
| downstream_bandwidth_usage | 入网带宽使用率 | 该指标用于统计测量对象入云平台的带宽使用率，以百分比为单位。入网带宽使用率=入网带宽指标/购买的带宽大小 | 0-100 | % | 不涉及 | bandwidth_id,publicip_id | 1分钟 |
| up_stream | 出网流量 | 该指标用于统计测试对象出云平台一分钟内的网络流量累加值（原指标为上行流量）。 | ≥ 0 | Byte | 1000(SI) | bandwidth_id,publicip_id | 1分钟 |
| down_stream | 入网流量 | 该指标用于统计测试对象入云平台一分钟内的网络流量累加值（原指标为下行流量）。 | ≥ 0 | Byte | 1000(SI) | bandwidth_id,publicip_id | 1分钟 |

## 子网IPv4地址监控指标

| 指标ID | 指标名称 | 指标含义 | 取值范围 | 单位 | 进制 | 维度 | 监控周期 |
|--------|----------|----------|----------|------|------|------|----------|
| subnet_ipv4_availability_used_number | 已使用IPv4地址数量 | 该指标用于统计子网内已使用的IPv4地址数量。 | ≥ 0 | 个 | 不涉及 | subnet_id | 30分钟 |
| subnet_ipv4_availability_remain_number | 剩余可使用IPv4地址数量 | 该指标用于统计子网内剩余可用的IPv4地址数量。 | ≥ 0 | 个 | 不涉及 | subnet_id | 30分钟 |
| subnet_ipv4_availability_total_number | 总IPv4地址数量 | 该指标用于统计子网内全部可用的IPv4地址数量。 | ≥ 0 | 个 | 不涉及 | subnet_id | 30分钟 |
| subnet_ipv4_availability_usage_percentage | 子网IPv4地址使用率 | 该指标用于统计子网内已使用IPv4地址数量占全部可用IPv4地址比例。 | 0-100 | % | 不涉及 | subnet_id | 30分钟 |

## 维度说明

| 维度名称 | 维度含义 | 获取方式 |
|----------|----------|----------|
| publicip_id | 弹性公网IP ID | 调用查询弹性公网IP详情API，从接口返回的响应参数中提取 |
| bandwidth_id | 带宽ID | 调用查询带宽API，从接口返回的响应参数中提取 |
| subnet_id | 子网ID | 调用查询子网列表API，从接口返回的响应参数中提取 |

## 使用说明

1. 命名空间: SYS.VPC
2. 监控周期: 1分钟（弹性公网IP和带宽原始指标）或30分钟（子网IPv4地址原始指标）
3. 维度层级: 云监控服务最大支持4个层级维度，维度编号从0开始，编号3为最深层级
4. 多层级维度查询示例:
   - 查询弹性公网IP的出网流量（up_stream），维度信息为"bandwidth_id,publicip_id"，表示bandwidth_id为0层，publicip_id为1层
   - API查询时: dim.0=bandwidth_id,{bandwidth_id值}&dim.1=publicip_id,{publicip_id值}
5. 进制说明: upstream_bandwidth、downstream_bandwidth、up_stream、down_stream 使用 1000(SI) 进制