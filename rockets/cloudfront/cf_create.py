from django.shortcuts import render, redirect
import boto3
import os
from rocket_admin.models import Serviceaws
from acm import ACM
from django.views.decorators.csrf import csrf_exempt
from ecr_functions import *
from ECR.views import *
from s3_functions import * 
from try_helm import *
from cloudfront import *  
from hosting.views import *
import time 


# AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)

aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
region_name = session.region_name

# 테스트페이지로 이동
def getTestPage(request):
    return render(request, 'cloudfront-test/testPage.html')



# 서비스명 가져오기
def getServiceName(request):
    userNo = request.session.get('UNO');
    
    userNo = int(userNo)
    
    print(userNo)
    
    serviceName = Serviceaws.objects.get(uno=1)
    print(serviceName)
    
    return serviceName.service_name


# CloudFront 생성하기
@csrf_exempt
def create_cloudfront_distribution(service_name,alb):
    # 변수 설정
    #optimize: 옵션으로 가져오기!
    serviceName = service_name
    print("serviceName: ", serviceName)
    cloudfrontDns=''

    # todo: 원본 도메인 주소 가져오기 = s3 엔드포인트 (from s3_bucket_create.py)
    # s3_website_endpoint: http://{bucket_name}.s3-website.{region_name}.amazonaws.com'
    s3_website_endpoint = "http://" + serviceName + ".s3-website." + region_name + ".amazonaws.com"
    origin_domain_name = s3_website_endpoint
    print("origin_domain_name: " + origin_domain_name)
    
    # cname : 대체 도메인 이름
    cname = serviceName + "rockets-yj.com" 
    viewer_protocol_policy = 'redirect-to-https' #뷰어 프로토콜 정책
    firewall_settings = False
    default_root_object = 'index.html'
    distribution_settings = None
    bucket_name = serviceName
    alb_dns = alb
    
    
    # acm 인증서 # todo: 윤지가 만든 ssl 인증서 가져오기
    ssl_certificate_arn = ACM.create_acm(serviceName) 
    
    print("ssl_certificate_arn: " + ssl_certificate_arn)
    # "arn:aws:acm:us-east-1:610264642862:certificate/98015bf7-2384-4ccd-9597-0b65d6a92873"     
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
        'CallerReference': f'{serviceName}', # 고유한 호출자 참조값, 호출 중복 방지
        'Origins': { # CloudFront 배포에 대한 원본 설정을 포함하는 항목
            'Quantity': 1, # 원본의 수
            'Items': [ # 원본에 대한 세부 정보
                {
                    'DomainName': alb_dns, # 도메인 이름 ex) d29d9qeen6l0km.cloudfront.net 이런식으로 생성됨
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
            'Items': [f'{serviceName}.rockets-yj.com', f'www.{serviceName}.rockets-yj.com'],  # 각 대체 도메인 이름이 포함
        },
        'WebACLId': '',  # 방화벽을 위한 웹 ACL ID} # 방화벽 설정 추가
        'ViewerCertificate': {
            'ACMCertificateArn': ssl_certificate_arn,  # ACM SSL/TLS 인증서 ARN #todo
            'SSLSupportMethod': 'sni-only',  # 'sni-only' 또는 'vip' / sni-only(서버이름 지원을 사용, 일반적으로 권장)
            'MinimumProtocolVersion': 'TLSv1.2_2021',

        },
        # 'Logging': {
        #     'Enabled': True,
        #     'IncludeCookies': False,
        #     'Bucket': bucket_name,
        #     'Prefix': 'cloudfront-logs/',
        # },
        'Comment': serviceName,  # 필수: 배포에 대한 주석
        'Enabled': True,  # 필수: 배포 활성화 여부
    }

    # 사용자 지정 CloudFront 설정이 전달되면 기본 설정과 병합
    if distribution_settings:
        default_distribution_settings.update(distribution_settings)

    try:
        # CloudFront 배포 생성
        response = client.create_distribution(DistributionConfig=default_distribution_settings)
        distribution_id = response['Distribution']['Id']
        print(f'CloudFront created successfully with ID: {distribution_id}')
        
        try:
            # CloudFront 배포가 생성되면 DNS 주소 가져오기  
            distribution_info = client.get_distribution(Id=distribution_id)
            cloudfrontDns = distribution_info['Distribution']['DomainName']
            print(f'CloudFront DNS: {cloudfrontDns}')
            
            return cloudfrontDns

        except Exception as e:
            print(f'CloudFront DNS 주소 출력 시 오류: {e}')
        
        
    except Exception as e:
        print(f'CloudFront 생성 시 오류: {e}')
    return cloudfrontDns


def addDomain(service_name,cloud_front):
    # Route 53 클라이언트를 생성합니다.
    client = session.client('route53')
    print(f'{service_name} : {cloud_front}')
    # 도메인에 레코드를 생성
    domain_name = 'rockets-yj.com'

    # 도메인 id 확인
    response = client.list_hosted_zones_by_name() # 모든 hosted Zone 을 가져옴
    hosted_zone_id = None

    for hosted_zone in response['HostedZones']:
        if hosted_zone['Name'] == domain_name + '.' :
            hosted_zone_id = hosted_zone['Id']
            break
        
    # /hostedzone/Z0958311YBP9BJL383S5 이런식으로 반환을 하기 때문에 앞의 /hostedzone/ 을 삭제한다
    hosted_zone_id = hosted_zone_id.split("/hostedzone/")[1]
    print(hosted_zone_id)

    # 로드밸런서의 주소
    cloud_front_dns = cloud_front

    response = client.change_resource_record_sets(
        HostedZoneId = hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': f'www.{service_name}.rockets-yj.com', # 원하는 도메인 이름
                        'Type': 'CNAME', # ipv4 주소는 A, dns 는 CNAME ,
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': cloud_front_dns
                            },
                        ],
                    }
                },
            ]
        }
    )
    return f'www.{service_name}.rockets-yj.com'




# @csrf_exempt
# def all_in_one(request):
    _service_name = request.POST.get('serviceName')
    _service_name = str(_service_name).lower()
    port = 8080
    # ecr 생성    
    try:
        userHosting(request)
        create_ecr_and_push_image(_service_name, region_name)
        
        _service = Serviceaws.objects.get(service_name=_service_name)
        
        try_helm.delete_folder(_service_name)
        try_helm.create_service(_service_name, _service.ecr_uri, _service.port, _service_name)
        try_helm.create_eks_nodegroup(_service_name, _service_name, 'eks-rockets')
        try_helm.helm_start(_service_name)
        time.sleep(10)                                   # 바로 LB 못 불러와서 잠시 후 불러오기 위해서
        _service.load_balancer_name = try_helm.get_load_balancer_dns(_service_name)
        _service.save()
        _service.cloudfront_dns = create_cloudfront_distribution(_service_name,_service.load_balancer_name)
        _service.save()
        _service.domain=addDomain(_service_name, _service.cloudfront_dns)
        _service.save()
        
    except Exception as e :
        return render (request,'cloudfront/testPage.html', {'error': f' 에러는: {e}'})
    
    return render(request, 'cloudfront-test/testPage.html',{'dns':_service.domain})

