import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core import serializers
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
import boto3
from django.http import HttpResponse
from rocket_admin.models import *
import os

# Create your views here.
# 사용자 서비스 상태 조회 페이지로 이동
# def userStatusPage(request):
#     return render(request, 'userStatus/userStatus.html')

# 사용자 서비스 


MAIN_DOMAIN = ".rockets-yj.com"

session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('AWS_REGION')
)


@csrf_exempt
def viewServiceList(request):
    userNo = request.session.get('UNO')
    serviceList = (
        Serviceaws.objects
        .filter(uno=userNo)
        .prefetch_related('backend_no', 'region_no', 'db_no')
    )
    return render(request, 'userStatus/userStatus.html', {'serviceList' : serviceList})


@csrf_exempt
def viewServiceInfoStatus(request):
    if request.method == 'POST':
        
        # 1. AWS EC2 인스턴스 목록 조회
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        
        # 2. serviceName이 포함된 인스턴스 목록 조회
        data = json.loads(request.body)
        svc_name = "eks-rockets-" + data.get('serviceName', '') + "-Node"

        instance_list = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
            if svc_name in next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), '')
        ]

        # 3. 인스턴스들의 상태 조회
        instance_status = {}
        for instance_id in instance_list:
            ec2_instance = boto3.resource('ec2').Instance(instance_id)  # 본인의 AWS 리전으로 변경
            state = ec2_instance.state['Name']
            instance_status[instance_id] = state

        # print("----------------------------instance_status:", instance_status)
        # 4. 인스턴스 상태에 따라 overallStatus 결정
        # 하나라도 running이면 running, 그렇지 않으면 terminated
        if all(status == 'terminated' for status in instance_status.values()):
            instance_status = 'terminated'
        else:
            instance_status = 'running'

        # overallStatus만 반환
        response_data = {'overallStatus': instance_status}
        return JsonResponse(response_data)
        
        
        

#사용자 서비스 상세 조회 - js. fetch.
@csrf_exempt
def viewServiceInfo(request):
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        serviceListId = data.get('serviceListId')

        print("serviceID:",serviceListId)
        
        # 사용자의 서비스 하나를 조회
        serviceData = (
            Serviceaws.objects
            .filter(service_no = serviceListId)
            .prefetch_related('backend_no','region_no', 'db_no')
        )
        
        
        # 1. AWS EC2 인스턴스 목록 조회
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        
        serviceInfo = [model_to_dict(svc) for svc in serviceData]
        
        
        # 서비스 상세 데이터 조회
        service_info = []
        service_info_list = []
        serviceName = ""
        
        for service in serviceData: 
            service_info = model_to_dict(service)
            service_info['region_name'] = service.region_no.region_name
            service_info['db_name'] = service.db_no.db_name
            service_info['backend_name'] = service.backend_no.backend_name
            # today = str(service.create_date)
            # service_info['today'] = today
            service_info['create_date'] = str(service.create_date)
            service_info['service_name'] = service.service_name
            serviceName = service_info['service_name']
        
                
            # 인스턴스 상태 불러오기
            # fixme: 인스턴스 아이디 가져오기!!!!!
            svc_name = "eks-rockets-" + serviceName + "-Node"

            instance_list = [
                instance['InstanceId']
                for reservation in response['Reservations']
                for instance in reservation['Instances']
                if svc_name in next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), '')
            ]

            # ec2 = boto3.client('ec2')
            # response = ec2.describe_instances(InstanceIds=[instance_id])
            # instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
            
                
            # 3. 인스턴스들의 상태 조회
            instance_status = {}
            for instance_id in instance_list:
                ec2_instance = boto3.resource('ec2').Instance(instance_id)  # 본인의 AWS 리전으로 변경
                state = ec2_instance.state['Name']
                instance_status[instance_id] = state
                
            # print("----------------------------instance_status:", instance_status)
            # 4. 인스턴스 상태에 따라 overallStatus 결정
            # 하나라도 running이면 running, 그렇지 않으면 terminated
            if all(status == 'terminated' for status in instance_status.values()):
                instance_status = 'terminated'
            else:
                instance_status = 'running'

            service_info_list.append(service_info)
            service_info_list.append(instance_status)    
        
    return JsonResponse({'serviceInfo' : service_info_list}, safe=False)
    
    
    
def delete_domain(service_name, cloud_front):

    # Route 53 클라이언트를 생성합니다.
    client = session.client('route53')

    # 도메인에 레코드를 생성

    # 도메인 id 확인
    response = client.list_hosted_zones_by_name() # 모든 hosted Zone 을 가져옴
    hosted_zone_id = None

    for hosted_zone in response['HostedZones']:
        if hosted_zone['Name'] == MAIN_DOMAIN[1:] + '.' :
            hosted_zone_id = hosted_zone['Id']
            break
        
    # /hostedzone/Z0958311YBP9BJL383S5 이런식으로 반환을 하기 때문에 앞의 /hostedzone/ 을 삭제한다
    hosted_zone_id = hosted_zone_id.split("/hostedzone/")[1]

    # 로드밸런서의 주소


    response = client.change_resource_record_sets(
        HostedZoneId = hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': f'www.{service_name}{MAIN_DOMAIN}', # 원하는 도메인 이름
                        'Type': 'CNAME', # ipv4 주소는 A, dns 는 CNAME ,
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': cloud_front
                            },
                        ],
                    }
                },
            ]
        }
    )


def delete_cloudFront(cloud_front_dns):
    # CloudFront 클라이언트 생성
    cloudfront = session.client('cloudfront')

    # CloudFront 배포 목록 가져오기
    response = cloudfront.list_distributions()

    # 도메인 이름으로 배포 ID, ETag 찾기
    distribution_id = None
    etag = None
    for distribution in response['DistributionList']['Items']:
        if distribution['DomainName'] == cloud_front_dns:
            distribution_id = distribution['Id']
            distribution_config = cloudfront.get_distribution_config(
                Id=distribution_id
                )
            etag=distribution_config['ETag']
            break
    
    # CloudFront 배포 삭제
    
    distribution_status = distribution.get('Status', '')
    print(distribution_status)
    if distribution_status == 'Deployed':
        print(f"CloudFront 배포 {distribution_id}는 현재 활성화되어 있습니다. 비활성화 중...")
        # 배포 비활성화
        distribution_details = cloudfront.get_distribution(
            Id=distribution_id
        )
        # DistributionConfig 가져오기
        distribution_config = distribution_details['Distribution']['DistributionConfig']
        # 배포 비활성화
        distribution_config['Enabled'] = False
        cloudfront.update_distribution(
            Id=distribution_id,
            DistributionConfig=distribution_config,
            IfMatch=etag,
        )
        print(f"CloudFront 배포 {distribution_id}가 성공적으로 비활성화되었습니다.")
    

    
    
    try:
        wait_time = 10
        cnt = 1
        while True:
            response = cloudfront.get_distribution(
                Id=distribution_id
            )
            if response['Distribution']['Status'] == 'InProgress':
                time.sleep(10)  # 10초 기다림
                print(wait_time*cnt)
                cnt+=1
            else:
                # 상태가 바뀌면 ETag 가 바뀌어서 다시 찾아야 함
                for distribution in response['DistributionList']['Items']:
                    if distribution['DomainName'] == cloud_front_dns:
                        distribution_id = distribution['Id']
                        distribution_config = cloudfront.get_distribution_config(
                            Id=distribution_id
                            )
                        etag=distribution_config['ETag']
                        break
                cloudfront.delete_distribution(
                    Id=distribution_id,
                    IfMatch=etag
                )
                print(f"CloudFront 배포 {distribution_id}가 성공적으로 비활성화되었습니다.")
                break
        print(f"CloudFront distribution {distribution_id} deleted successfully.")
    except Exception as e:
        print(f"CloudFront distribution with domain name {cloud_front_dns} not found. error: {e}")
    


def delete_all_objects_in_bucket(bucket_name):
    # boto3 S3 클라이언트 생성
    s3 = session.client('s3')

    try:
        # 버킷 안의 객체 목록 가져오기
        response = s3.list_objects_v2(Bucket=bucket_name)

        # 버킷 안의 모든 객체(파일, 디렉토리, zip파일 등) 전체 삭제 후 결과 print
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Object '{obj['Key']}' deleted from bucket '{bucket_name}'")

        print(f"All objects deleted from bucket '{bucket_name}'")
    except Exception as e:
        print(f"Error deleting objects from bucket '{bucket_name}': {e}")



def delete_s3_bucket(bucket_name):
    # boto3 S3 클라이언트 생성
    s3 = session.client('s3')
    
    try:
        # 버킷 안의 모든 객체 삭제
        delete_all_objects_in_bucket(bucket_name)

        # S3 버킷 삭제
        s3.delete_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting S3 bucket '{bucket_name}': {e}")
    
    
    
def delete_ecr(repository_name):
    ecr_client = session.client('ecr')
    
    print("delete_ecr :", repository_name)
    

    try:
        # ECR 리포지토리 삭제
        response = ecr_client.delete_repository(repositoryName=repository_name, force=True)
        print(f'삭제 성공 {response}')
        return response
    except Exception as e:
        print(f'삭제에 실패했습니다: {e}')
        return {'error_message': str(e)}
    
@csrf_exempt
def serviceDelete(request):
    data = json.loads(request.body.decode('utf-8'))
    serviceId = data.get('serviceId')
    user_data = Serviceaws.objects.get(service_no=serviceId)
    print(user_data.service_name)
    print(user_data.load_balancer_name)
    delete_domain(user_data.service_name, user_data.cloudfront_dns)
    delete_s3_bucket(user_data.service_name+MAIN_DOMAIN)
    #delete_cloudFront('d23wsehoeia6bo.cloudfront.net')
    delete_ecr(user_data.service_name)
    #delete_s3_bucket(user_data.service_name+MAIN_DOMAIN)
    # for i in range (5,10):
    #     delete_s3_bucket(f'iloverocketdan{i}'+MAIN_DOMAIN)
    
    
    user_data.delete()
    
    return JsonResponse({'message': '삭제 성공!!!!!!!!!!!!!'}, status=200)
