from django.shortcuts import render, redirect
import boto3
import os
from rocket_admin.models import Serviceaws


# AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)

aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
region_name = session.region_name


# 서비스명 가져오기
def getServiceName(request):
    userNo = request.session.get('UNO');
    
    serviceName = (
        Serviceaws.objects.filter(userNo=userNo).values('serviceName').first()
    )
    
    return serviceName


# CloudFront 생성하기
def create_cloudfront_distribution():
    # 변수 설정
    #optimize: 옵션으로 가져오기!
    serviceName = getServiceName();
    print("serviceName: ", serviceName)

    # todo: 원본 도메인 주소 가져오기 = s3 엔드포인트 (from s3_bucket_create.py)
    # s3_website_endpoint: http://{bucket_name}.s3-website.{region_name}.amazonaws.com'
    s3_website_endpoint = "http://" + serviceName + ".s3-website." + region_name + ".amazonaws.com"
    origin_domain_name = s3_website_endpoint
    print("origin_domain_name: " + origin_domain_name)
    
    # cname : 대체 도메인 이름
    cname = serviceName + "rockets-yj.com" 
    viewer_protocol_policy = 'redirect-to-https' #뷰어 프로토콜 정책
    firewall_settings = False
    ssl_certificate_arn = "arn:aws:acm:us-east-1:610264642862:certificate/98015bf7-2384-4ccd-9597-0b65d6a92873" # todo: 윤지가 만든 ssl 인증서 가져오기
    default_root_object = 'index.html'
    distribution_settings = None
    bucket_name = serviceName
    
    '''
    # todo: 
    # 1) 인증서 넣기  
    # 2) 로드밸런서 넣기  
    # 3) s3 엔드포인트 넣기
    '''
    
    
    # AWS CloudFront 클라이언트 생성
    client = boto3.client('cloudfront')


    # 기본 CloudFront 배포 설정
    default_distribution_settings = {
        'CallerReference': 'your-unique-caller-reference', # 고유한 호출자 참조값, 호출 중복 방지
        'Origins': { # CloudFront 배포에 대한 원본 설정을 포함하는 항목
            'Quantity': 1, # 원본의 수
            'Items': [ # 원본에 대한 세부 정보
                {
                    'DomainName': serviceName + "cloudfront.net", # 도메인 이름 ex) d29d9qeen6l0km.cloudfront.net 이런식으로 생성됨
                    'Id': serviceName, # 원본을 식별하는 고유 ID, 해당 원본을 참조
                    'CustomOriginConfig': { # 사용자 지정 설정
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only', # 원본과의 통신 시 사용할 프로토콜 정책
                    }
                },
            ],
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': serviceName, # 해당 캐시 동작이 적용되는 원본 ID / '' -> 자동할당
            'ForwardedValues': { # CloudFront가 요청을 원본에 전달할 때 어떤 값들을 전달할지 설정
                'QueryString': True, # 쿼리문자열 포함 여부 (False : 설정x)
                'Cookies': {
                    'Forward': 'none', # 쿠키값 (none: 전달 안함)
                },
            },
            'ViewerProtocolPolicy': viewer_protocol_policy,  # 뷰어와 CloudFront 사이의 통신에 사용할 프로토콜
            'MinTTL': 0, # 최소 TTL(Time-to-Live). 캐시에서 가져온 리소스를 얼마동안 유지할지 결정 (0 : 항상 새로운 리소스를 가져와 원본 서버에 갱신)
        },
        # 루트 경로('/')로 요청 시 기본으로 제공될 객체
        'DefaultRootObject': default_root_object, # 함수 호출 시 전달되는 인자
        'Aliases': { # CloudFront 배포에 대한 대체 도메인 이름(CNAME)  #todo
            'Quantity': 2, # 대체 도메인 이름 수
            'Items': ['youngtesttest12345.rockets-yj.com', 'www.youngtesttest12345.rockets-yj.com'],  # 각 대체 도메인 이름이 포함
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


create_cloudfront_distribution()