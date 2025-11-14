VPC (虚拟私有云) API 文档:

常用端点:
1. 查询VPC列表:
- action: 'v3/{project_id}/vpc/vpcs'
- method: GET
- 功能: 当您的VPC创建成功后，您可以通过调用此接口查询所有VPC信息，包括VPC名称、ID、网段等。查询提交请求的租户有权限查看的所有vpc信息，单次查询最多返回2000条数据，超过2000后会返回分页标记。
- 路径参数:
  * project_id (必选): VPC所属的项目ID。获取方式请参见获取项目ID文档
- 查询参数 (可选):
  * limit (Integer): 每页返回的个数。取值范围：0-2000
  * marker (String): 分页查询起始的资源ID，为空时查询第一页。取值范围：VPC资源ID
  * id (Array of strings): VPC资源ID，可以使用该字段过滤VPC
  * name (Array of strings): VPC的名称信息，可以使用该字段过滤VPC
  * description (Array of strings): VPC的描述信息，可以使用该字段过滤VPC
  * cidr (Array of strings): VPC的网段信息，可以使用该字段过滤VPC
- 响应格式:
  * request_id (String): 请求ID
  * vpcs (Array): 查询VPC列表响应体，每个VPC对象包含以下主要字段:
    - id (String): VPC资源ID。VPC创建成功后，会生成一个VPC ID，是VPC对应的唯一标识。取值范围：带"-"的UUID格式
    - name (String): VPC的名称。取值范围：0-64个字符，支持数字、字母、中文、_(下划线)、-（中划线）、.（点）
    - description (String): VPC的描述信息。取值范围：0-255个字符，不能包含"<"和">"
    - cidr (String): VPC的网段。取值范围：10.0.0.0/8~24, 172.16.0.0/12~24, 192.168.0.0/16~24
    - status (String): VPC的状态，可选值:
      * CREATING: 创建中
      * OK: 正常
      * ERROR: 异常
    - enterprise_project_id (String): 企业项目ID
    - created_at (String): VPC创建时间，ISO8601格式
    - updated_at (String): VPC更新时间，ISO8601格式
    - tags (Array): 标签列表，每个标签包含:
      * key (String): 标签键
      * value (String): 标签值
  * page_info (Object): 分页信息，包含:
    - next_marker (String): 下一页的分页标记
    - current_count (Integer): 当前页的记录数
- 示例:
  * 查询所有VPC: GET /v3/{project_id}/vpc/vpcs
  * 按ID过滤: GET /v3/{project_id}/vpc/vpcs?id=vpc-xxxxx
  * 按名称过滤: GET /v3/{project_id}/vpc/vpcs?name=my-vpc
  * 按网段过滤: GET /v3/{project_id}/vpc/vpcs?cidr=192.168.0.0/16
  * 分页查询: GET /v3/{project_id}/vpc/vpcs?marker={vpc_id}&limit=50
  * 组合查询: GET /v3/{project_id}/vpc/vpcs?name=test&limit=20