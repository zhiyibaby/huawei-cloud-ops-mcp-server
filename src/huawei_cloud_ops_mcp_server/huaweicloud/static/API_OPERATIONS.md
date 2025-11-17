# 常用操作示例说明文档

1 查看所有ECS实例:
```
service: 'ecs'
action: 'v1.1/{project_id}/cloudservers/detail'
method: 'GET'
```

2 查看所有VPC:
```
service: 'vpc'
action: 'v3/{project_id}/vpc/vpcs'
method: 'GET'
```

3 查看所有RDS实例:
```
service: 'rds'
action: 'v3/{project_id}/instances'
method: 'GET'
```

4 查看所有云硬盘:
```
service: 'evs'
action: 'v2/{project_id}/cloudvolumes/detail'
method: 'GET'
```

5 查看所有负载均衡器:
```
service: 'elb'
action: 'v3/{project_id}/elb/loadbalancers'
method: 'GET'
```

6 查看所有OBS桶:
```
service: 'obs'
action: '/'
method: 'GET'
```

7 查看所有弹性公网IP:
```
service: 'eip'
action: 'v3/{project_id}/eip/publicips'
method: 'GET'
```

8 查看所有DDS实例:
```
service: 'dds'
action: 'v3/{project_id}/instances'
method: 'GET'
```

9 查看所有CSS集群:
```
service: 'css'
action: 'v1.0/{project_id}/clusters'
method: 'GET'
```

10 查看所有DCS实例:
```
service: 'dcs'
action: 'v2/{project_id}/instances'
method: 'GET'
```

11 查询监控数据 (CES):
```
service: 'ces'
action: 'V1.0/{project_id}/metric-data'
method: 'GET'
params: {
  'namespace': 'SYS.ECS',
  'metric_name': 'cpu_util',
  'dim.0': 'instance_id,12345678-1234-1234-1234-123456789012',
  'from': 1442341200000,
  'to': 1442344800000,
  'period': 300,
  'filter': 'average'
}
```

使用 get_huawei_api_docs() 获取详细API文档。