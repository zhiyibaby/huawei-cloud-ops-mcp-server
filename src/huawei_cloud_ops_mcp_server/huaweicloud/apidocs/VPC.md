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
  
2. 查询安全组列表:
- action: 'v3/{project_id}/vpc/security-groups'
- method: GET
- 功能: 通过该接口查询指定项目下可见的所有安全组信息，返回安全组名称、ID、描述、企业项目等属性。每次最多返回2000条记录，超过则需使用分页标记继续查询。
- 路径参数:
  * project_id (必选): 安全组所属项目ID。
- 查询参数 (可选):
  * limit (Integer): 每页返回的记录数，范围0-2000。
  * marker (String): 分页起始资源ID，留空表示查询第一页。
  * id (Array of strings): 精确匹配安全组ID，支持多个ID。
  * name (Array of strings): 精确匹配安全组名称，支持多个名称。
  * description (Array of strings): 按描述过滤安全组。
  * enterprise_project_id (String): 按企业项目ID过滤。可使用"0"表示默认项目，或"all_granted_eps"查询当前账号可见的全部企业项目。
- 响应格式:
  * request_id (String): 请求ID。
  * security_groups (Array): 安全组列表，单个安全组包含:
    - id (String): 安全组ID（UUID）。
    - name (String): 安全组名称，1-64字符。
    - description (String): 安全组描述，0-255字符，不可包含"<"或">"。
    - project_id (String): 所属项目ID。
    - enterprise_project_id (String): 所属企业项目ID，或"0"。
    - created_at / updated_at (String): 创建、更新时间，UTC ISO8601格式。
    - security_group_rules (Array): 关联的入/出方向规则。
  * page_info (Object): 分页信息，含next_marker与current_count。
- 示例:
  * 基础查询: GET /v3/{project_id}/vpc/security-groups
  * 按ID过滤: GET /v3/{project_id}/vpc/security-groups?id=sg-xxxxx
  * 按名称过滤: GET /v3/{project_id}/vpc/security-groups?name=my-sg
  * 分页查询: GET /v3/{project_id}/vpc/security-groups?marker={sg_id}&limit=100
  
3. 查询安全组详情:
- action: 'v3/{project_id}/vpc/security-groups/{security_group_id}'
- method: GET
- 功能: 查询单个安全组的完整信息，包括标签、入出方向规则、企业项目归属等，常用于排查规则配置或展示安全组详情。
- 路径参数:
  * project_id (必选): 安全组所属项目ID。
  * security_group_id (必选): 目标安全组ID。
- 请求体: 无。
- 响应格式:
  * request_id (String): 请求ID。
  * security_group (Object): 安全组详情，字段包括:
    - id / name / description / project_id / enterprise_project_id: 基本属性。
    - created_at / updated_at (String): 创建与更新时间，UTC ISO8601格式。
    - tags (Array): 标签列表，每项含key、value。
    - security_group_rules (Array): 规则列表，包含方向direction、协议protocol、端口port_range、远端remote_ip_prefix或remote_group_id、ethertype等。
- 示例:
  * 查询详情: GET /v3/{project_id}/vpc/security-groups/sg-xxxxx