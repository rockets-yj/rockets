#s3버킷생성 및 policy 설정

import boto3
import os
import json

MAIN_DOMAIN = ".rockets-yj.com"

#AWS 환경변수 session으로 가져오기 
# session = boto3.Session (
    
#     aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
#     aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
#     region_name= os.environ.get('AWS_REGION')
# )

# 버킷 이름 및 정책 설정
#bucket_name은 DB에서 서비스명으로 받아와야 함 
bucket_name = 'testtestestsongsongsong' + MAIN_DOMAIN
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

# aws_access_key_id="AKIAY4FU3OUXBF7JOCX3"
# aws_secret_access_key="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" 
# region_name="ap-northeast-2"


# # Boto3 클라이언트 생성
# s3_client = boto3.client('s3', aws_access_key_id, aws_secret_access_key, region_name)

# S3 버킷 생성
# s3_client.create_bucket(Bucket=bucket_name)

# # 버킷 정책 설정
# s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
