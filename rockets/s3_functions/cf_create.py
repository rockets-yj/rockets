import boto3

def create_cloudfront_distribution(origin_domain_name, endpoint, cname=None, viewer_protocol_policy='redirect-to-https', firewall_settings=None, ssl_certificate_arn=None, default_root_object='index.html', distribution_settings=None):
    # 변수 설정
    # todo: DB에서 서비스 네임 불러오기 (서비스이름.rockets-yj.com)
    origin_domain_name = ""
    
    
    # AWS CloudFront 클라이언트 생성
    client = boto3.client('cloudfront')


    # 기본 CloudFront 배포 설정
    default_distribution_settings = {
        'CallerReference': 'your-unique-caller-reference', # 고유한 호출자 참조값, 호출 중복 방지
        'Origins': { # CloudFront 배포에 대한 원본 설정을 포함하는 항목
            'Quantity': 1, # 원본의 수
            'Items': [ # 원본에 대한 세부 정보
                {
                    'DomainName': origin_domain_name, # 도메인 이름
                    'Id': 'Custom-origin', # 원본을 식별하는 고유 ID, 해당 원본을 참조
                    'CustomOriginConfig': { # 사용자 지정 설정
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'https-only', # 원본과의 통신 시 사용할 프로토콜 정책
                    }
                },
            ],
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'Custom-origin', # 해당 캐시 동작이 적용되는 원본 ID
            'ForwardedValues': { # CloudFront가 요청을 원본에 전달할 때 어떤 값들을 전달할지 설정
                'QueryString': False, # 쿼리문자열 포함 여부 (False : 설정x)
                'Cookies': {
                    'Forward': 'none', # 쿠키값 (none: 전달 안함)
                },
            },
            'ViewerProtocolPolicy': viewer_protocol_policy,  # 뷰어와 CloudFront 사이의 통신에 사용할 프로토콜
            'MinTTL': 0, # 최소 TTL(Time-to-Live). 캐시에서 가져온 리소스를 얼마동안 유지할지 결정 (0 : 항상 새로운 리소스를 가져와 원본 서버에 갱신)
        },
        # 루트 경로('/')로 요청 시 기본으로 제공될 객체
        'DefaultRootObject': default_root_object, # 함수 호출 시 전달되는 인자
        'Aliases': { # CloudFront 배포에 대한 대체 도메인 이름(CNAME)  #TODO
            'Quantity': 1, # 대체 도메인 이름 수
            'Items': [cname] if cname else [],  # 각 대체 모데인 이름이 포함
        },
        'Firewall': { # 기본 방화벽 설정 #todo:
            'Enabled': False,  # 방화벽 활성화 여부 : 비활성화
            # 'WebACLId': 'your-web-acl-id',  # 방화벽을 위한 웹 ACL ID} # 방화벽 설정 추가
        },
        'ViewerCertificate': {
            'ACMCertificateArn': ssl_certificate_arn,  # ACM SSL/TLS 인증서 ARN #TODO
            'SSLSupportMethod': 'sni-only',  # 'sni-only' 또는 'vip' / sni-only(서버이름 지원을 사용, 일반적으로 권장)
        },
        'Logging': {
            'Enabled': True,
            'IncludeCookies': False,
            'Bucket': 'my-logs-bucket',
            'Prefix': 'cloudfront-logs/',
        },
        # 추가적인 설정은 필요에 따라 구성할 수 있습니다.
    }

    # 사용자 지정 CloudFront 설정이 전달되면 기본 설정과 병합
    if distribution_settings:
        default_distribution_settings.update(distribution_settings)

    try:
        # CloudFront 배포 생성
        response = client.create_distribution(DistributionConfig=default_distribution_settings)
        distribution_id = response['Distribution']['Id']
        print(f'CloudFront distribution created successfully with ID: {distribution_id}')
    except Exception as e:
        print(f'Error creating CloudFront distribution: {e}')

    # 예시: 사용자 정의 SSL 인증서를 선택하여 CloudFront 배포 생성
    additional_settings = {
        'Comment': 'My CloudFront Distribution',
        'Logging': {
            'Enabled': True,
            'IncludeCookies': False,
            'Bucket': 'my-logs-bucket',
            'Prefix': 'cloudfront-logs/',
        },
        'Firewall': {
            'Enabled': True,
            'WebACLId': 'your-web-acl-id',
        },
        'ViewerCertificate': {
            'ACMCertificateArn': 'your-acm-certificate-arn',  # ACM SSL/TLS 인증서 ARN 입력
            'SSLSupportMethod': 'sni-only',
        },
        # 다른 설정들...
    }

    # CloudFront 배포 생성 함수 호출
    create_cloudfront_distribution('example.com', 'your-origin-endpoint', cname='cdn.example.com', distribution_settings=additional_settings)
