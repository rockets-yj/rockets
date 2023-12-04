import boto3
import os
import json

# AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)

aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
region_name = session.region_name


def create_s3_bucket(hosting_name):
    # 버킷 이름 및 정책 설정, hosting_name은 hosting 등록시 name으로
    MAIN_DOMAIN = ".rockets-yj.com" 
    bucket_name = hosting_name + MAIN_DOMAIN
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    # Boto3 클라이언트 생성
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    # S3 버킷 생성 
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})

    # S3 권한>퍼블릭 액세스 차단을 비활성으로 변경
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )

    # 버킷 정책 설정
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

    # 정적 웹 사이트 호스팅 활성화 설정
    s3_client.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'}
        }
    )

    # 정적 웹 사이트 호스팅 앤드포인트 출력
    print(f's3_website_endpoint: http://{bucket_name}.s3-website.{region_name}.amazonaws.com')
    
    return 1
# 함수 호출 ()안에 hosting시 등록한 서비스 네임 DB와 연결하기 
# create_s3_bucket('youngtesttest12345')




def printEndpoint() :
    # todo: hosting name 바꾸기
    # hosting_name = "lej_test123455"
    # create_s3_bucket(hosting_name)
    ept = "http://youngtesttest12345.rockets-yj.com.s3-website.ap-northeast-2.amazonaws.com"
    return ept

