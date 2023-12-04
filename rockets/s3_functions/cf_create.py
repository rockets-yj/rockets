from django.shortcuts import render, redirect
import boto3
# from rocket_admin.models import Serviceaws
from .s3_bucket_create_def import printEndpoint


# def getServiceName(request):
#     userNo = request.session.get('UNO');
    
#     serviceName = (
#         Serviceaws.objects.filter(userNo=userNo).values('serviceName').first()
#     )
    
#     return serviceName



def create_cloudfront_distribution():
    # 변수 설정
    #optimize: 옵션으로 가져오기!
    origin_domain_name = printEndpoint() # todo: 원본 도메인 주소 가져오기 = s3 엔드포인트 (from s3_bucket_create.py)\
    print(origin_domain_name)
    
    cname="yountest1234.rockets-yj.com" #fixme: serviceName + "rockets-yj.com"
    viewer_protocol_policy='redirect-to-https'
    firewall_settings=False
    ssl_certificate_arn="arn:aws:acm:us-east-1:610264642862:certificate/258da75d-d601-4d6c-85a5-ff9395e59ad2" # todo: 윤지가 만든 ssl 인증서 가져오기
    default_root_object='index.html'
    distribution_settings=None
    bucket_name="youngtesttest12345"
    
    
    #fixme
    serviceName = "test1234"
    
    # AWS CloudFront 클라이언트 생성
    client = boto3.client('cloudfront')


    # 기본 CloudFront 배포 설정
    default_distribution_settings = {
        'CallerReference': 'your-unique-caller-reference', # 고유한 호출자 참조값, 호출 중복 방지
        'Origins': { # CloudFront 배포에 대한 원본 설정을 포함하는 항목
            'Quantity': 1, # 원본의 수
            'Items': [ # 원본에 대한 세부 정보
                {
                    'DomainName': 'youngtesttest12345.', # 도메인 이름
                    'Id': serviceName, # 원본을 식별하는 고유 ID, 해당 원본을 참조
                    # 'CustomOriginConfig': { # 사용자 지정 설정
                    #     'HTTPPort': 80,
                    #     'HTTPSPort': 443,
                    #     'OriginProtocolPolicy': 'https-only', # 원본과의 통신 시 사용할 프로토콜 정책
                    # }
                },
            ],
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': serviceName, # 해당 캐시 동작이 적용되는 원본 ID / '' -> 자동할당
            # 'ForwardedValues': { # CloudFront가 요청을 원본에 전달할 때 어떤 값들을 전달할지 설정
            #     'QueryString': False, # 쿼리문자열 포함 여부 (False : 설정x)
            #     'Cookies': {
            #         'Forward': 'none', # 쿠키값 (none: 전달 안함)
            #     },
            # },
            'ViewerProtocolPolicy': viewer_protocol_policy,  # 뷰어와 CloudFront 사이의 통신에 사용할 프로토콜
            'MinTTL': 0, # 최소 TTL(Time-to-Live). 캐시에서 가져온 리소스를 얼마동안 유지할지 결정 (0 : 항상 새로운 리소스를 가져와 원본 서버에 갱신)
        },
        # 루트 경로('/')로 요청 시 기본으로 제공될 객체
        'DefaultRootObject': default_root_object, # 함수 호출 시 전달되는 인자
        'Aliases': { # CloudFront 배포에 대한 대체 도메인 이름(CNAME)  #todo
            'Quantity': 1, # 대체 도메인 이름 수
            'Items': [cname] if cname else [],  # 각 대체 도메인 이름이 포함
        },
        'WebACLId': '',  # 방화벽을 위한 웹 ACL ID} # 방화벽 설정 추가
        'ViewerCertificate': {
            'ACMCertificateArn': ssl_certificate_arn,  # ACM SSL/TLS 인증서 ARN #todo
            'SSLSupportMethod': 'sni-only',  # 'sni-only' 또는 'vip' / sni-only(서버이름 지원을 사용, 일반적으로 권장)
        },
        # 'Logging': {
        #     'Enabled': True,
        #     'IncludeCookies': False,
        #     'Bucket': bucket_name,
        #     'Prefix': 'cloudfront-logs/',
        # },
        'Comment': 'My CloudFront Distribution',  # 필수: 배포에 대한 주석
        'Enabled': True,  # 필수: 배포 활성화 여부
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
    # additional_settings = {
    #     'Comment': 'My CloudFront Distribution',
    #     'Logging': {
    #         'Enabled': True,
    #         'IncludeCookies': False,
    #         'Bucket': 'my-logs-bucket',
    #         'Prefix': 'cloudfront-logs/',
    #     },
    #     'Firewall': {
    #         'Enabled': True,
    #         'WebACLId': 'your-web-acl-id',
    #     },
    #     'ViewerCertificate': {
    #         'ACMCertificateArn': 'your-acm-certificate-arn',  # ACM SSL/TLS 인증서 ARN 입력
    #         'SSLSupportMethod': 'sni-only',
    #     },
    #     # 다른 설정들...
    # }

    # CloudFront 배포 생성 함수 호출
    # create_cloudfront_distribution('example.com', 'your-origin-endpoint', cname='cdn.example.com', distribution_settings=additional_settings)


create_cloudfront_distribution()