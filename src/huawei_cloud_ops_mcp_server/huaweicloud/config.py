from huawei_cloud_ops_mcp_server.huaweicloud.apidocs import SUPPORTED_SERVICES

PROJECT_ID = {
    '非洲-开罗': {
        'region': 'af-north-1',
        'project_id': 'fd83d445aa5b486e882506893bda6e04'
    },
    '非洲-约翰内斯堡': {
        'region': 'af-south-1',
        'project_id': 'da2f77ae9c2e4a80a1b54d9697e341e3'
    },
    '中国-香港': {
        'region': 'ap-southeast-1',
        'project_id': '1ff14256c93a4ce4a71f97861a19c67f'
    },
    '亚太-曼谷': {
        'region': 'ap-southeast-2',
        'project_id': '119c23bdbb45404090361532860195a2'
    },
    '亚太-新加坡': {
        'region': 'ap-southeast-3',
        'project_id': 'b91f7f7b97ad423b8b1594c877751ff8'
    },
    '亚太-雅加达': {
        'region': 'ap-southeast-4',
        'project_id': '7e1cb88367fa41d589447903a27a4069'
    },
    '亚太-马尼拉': {
        'region': 'ap-southeast-5',
        'project_id': 'a8243d342af44e728926cdd45b0d8f46'
    },
    '华东-上海二': {
        'region': 'cn-east-2',
        'project_id': 'b47f428e03da42f9acf17fbdaf65b4b3'
    },
    '华东-上海一': {
        'region': 'cn-east-3',
        'project_id': '05eb31eb5b0025df2fffc018710c5aa4'
    },
    '华东二': {
        'region': 'cn-east-4',
        'project_id': '18651faca4404dd0bdf286c1d1070c41'
    },
    '华东-青岛': {
        'region': 'cn-east-5',
        'project_id': '718fea843ceb4f53834152de31b818e2'
    },
    '华北-北京一': {
        'region': 'cn-north-1',
        'project_id': '96b3d3a55d184f23ace3d293a4105109'
    },
    '华北三': {
        'region': 'cn-north-12',
        'project_id': 'a0726ee3d6ab48ab927c1df7f9c02a51'
    },
    '华北-北京四': {
        'region': 'cn-north-4',
        'project_id': 'f033a60e8a8e496da41a890e0e013950'
    },
    '华北-乌兰察布一': {
        'region': 'cn-north-9',
        'project_id': '0d79ac54e100901b2fd6c018b1d626ee'
    },
    '华南-广州': {
        'region': 'cn-south-1',
        'project_id': '65305edb3fdc4db08426fe4d4e00a4ba'
    },
    '华南-广州-友好用户环境': {
        'region': 'cn-south-4',
        'project_id': '1fe377bf0ca84b7e822bc904406e6210'
    },
    '西南-贵阳一': {
        'region': 'cn-southwest-2',
        'project_id': 'db5d024bd0b14dc9ac58287019ccbd85'
    },
    '拉美-墨西哥城二': {
        'region': 'la-north-2',
        'project_id': 'ea822d97dda346cc93c18b6daedf4f72'
    },
    '拉美-圣地亚哥': {
        'region': 'la-south-2',
        'project_id': '0904c365dc80f34a2f01c0182d38eacf'
    },
    '中东-利雅得': {
        'region': 'me-east-1',
        'project_id': '3ab56bd3105b4552ab91ef1905a7f5ca'
    },
    '拉美-墨西哥城一': {
        'region': 'na-mexico-1',
        'project_id': '88ca6968ff8c4c8f808639de14549de3'
    },
    '拉美-圣保罗一': {
        'region': 'sa-brazil-1',
        'project_id': '0904c35e8580f5b62f40c0187ad1de8c'
    },
    '土耳其-伊斯坦布尔': {
        'region': 'tr-west-1',
        'project_id': '7fde4c3ebe6142d5995f041b93dd9c51'
    }
}


def base_url(service: str, zone: str) -> tuple[str, str, str]:
    '''
    获取华为云 API 基础 URL

    Args:
        service: 服务类型（会自动转换为小写进行验证）
        zone: 区域名称

    Returns:
        tuple[str, str, str]: (project_id, region, url)
    '''
    # 同时获取项目的 region 和 project_id
    match = next(
        (
            v
            for k, v in PROJECT_ID.items()
            if zone in k
        ),
        None
    )

    if not match or 'project_id' not in match or 'region' not in match:
        raise ValueError(
            'project_id 或 region 参数未能从 zone 信息中获取。请传入有效的华为云项目ID与区域。'
        )

    region = match['region']
    project_id = match['project_id']

    service_l = service.lower()
    if service_l not in SUPPORTED_SERVICES:
        supported_services = ', '.join(sorted(SUPPORTED_SERVICES))
        raise ValueError(
            f'错误: 不支持的服务类型 "{service}".'
            f'支持的服务: {supported_services}'
        )

    # 使用小写的服务名称构建 URL
    url = f'https://{service_l}.{region}.myhuaweicloud.com'
    return project_id, region, url
