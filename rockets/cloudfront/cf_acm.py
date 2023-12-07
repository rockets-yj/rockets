from django.shortcuts import render, redirect
import boto3
import os
from rocket_admin.models import Serviceaws
from try_helm import *

# AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)

aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
region_name = session.region_name


# CloudFront 인증서 생성
# acm
def create_acm_certificate(request, service_name):
    
    userNo = request.session.get('UNO');
    
    service = Serviceaws.objects.get(uno=userNo)
    print("service: ", service)

    #todo: 1. Helm 사전작업
    # 1-1) 서비스 생성하기 _헬름
    image = service.ecr_uri
    port = service.port
    email = service.email
    try_helm.create_service(service_name, image, port, email)
        



    # 1-2) eks nodegroup 생성하기

    #todo: 2. Helm
    # 2-1) 헬름 시작
    # 2-2) 로드밸런서 dns 가져오기
    # 2-3) 로드밸런서 dns, DB에 저장하기

    #todo: 3. ACM 인증서
    # 3-1) 인증서 요청
    # 3-2) dns 생성하기
    # 3-3) CloudFront에 연결하기