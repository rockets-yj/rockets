from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core import serializers
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
import boto3
from django.http import HttpResponse

# Create your views here.
# 사용자 서비스 상태 조회 페이지로 이동
# def userStatusPage(request):
#     return render(request, 'userStatus/userStatus.html')

# 사용자 서비스 

@csrf_exempt
def viewServiceList(request):
    userNo = request.session.get('UNO')
    serviceList = (
        Serviceaws.objects
        .filter(uno=userNo)
        .prefetch_related('backend_no', 'region_no', 'db_no')
    )
    return render(request, 'userStatus/userStatus.html', {'serviceList' : serviceList})

# @csrf_exempt
# def viewServiceList(request):
    
#     # userNo를 받아와서 해당 사용자의 서비스 목록 조회하기
#     userNo = request.session.get('UNO')
#     # userNo = 1
    
#     serviceList = (
#         Serviceaws.objects
#         .filter(uno=userNo)
#         .prefetch_related('backend_no', 'region_no', 'db_no')
#     )

#     # EC2 인스턴스 상태 가져오기
#     instance_id = 'i-04f9793101da30171'
#     ec2 = boto3.client('ec2')
    
#     try:
#         response = ec2.describe_instances(InstanceIds=[instance_id])
#         reservation = response['Reservations'][0]
#         instance = reservation['Instances'][0]
#         instance_status = instance['State']['Name']
#         print('Instance status', instance_status)
        
#     except (IndexError, KeyError):
#         # IndexError: list index out of range
#         # KeyError: 'Reservations' 또는 'Instances' 키가 없는 경우
#         instance_status = 'Status Not Found'
#         print('Instance status', instance_status)

#     # Django에서 JSON으로 데이터를 반환
#     service_info = []
#     service_info_list = []
    
#     for service in serviceList: 
#         service_info = model_to_dict(service)
#         service_info['region_name'] = service.region_no.region_name
#         service_info['db_name'] = service.db_no.db_name
#         service_info['backend_name'] = service.backend_no.backend_name
#         # today = str(service.create_date)
#         # service_info['today'] = today
#         service_info['create_date'] = str(service.create_date)
        
#          # 인스턴스 상태 불러오기
#         # fixme: 인스턴스 아이디 가져오기!!!!!
#         instance_id = 'i-0cde9652658517c13'
#         ec2 = boto3.client('ec2')
#         # response = ec2.describe_instances(InstanceIds=[instance_id])
#         # instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
#         try:
#             response = ec2.describe_instances(InstanceIds=[instance_id])
#             reservation = response['Reservations'][0]
#             instance = reservation['Instances'][0]
#             instance_status = instance['State']['Name']
#         except (IndexError, KeyError):
#             # IndexError: list index out of range
#             # KeyError: 'Reservations' 또는 'Instances' 키가 없는 경우
#             instance_status = 'Status Not Found'
        
        
#         service_info_list.append(service_info)
#         service_info_list.append(instance_status)    

#     return JsonResponse({'serviceList': service_info_list}, safe=False)

@csrf_exempt
def viewServiceInfoStatus(request):
    if request.method == 'GET':
        
        # fixme: 인스턴스 아이디 가져오기!!!!!
        instance_id = 'i-0cde9652658517c13'
        ec2 = boto3.client('ec2')
        # response = ec2.describe_instances(InstanceIds=[instance_id])
        # instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            reservation = response['Reservations'][0]
            instance = reservation['Instances'][0]
            instance_status = instance['State']['Name']
        except (IndexError, KeyError):
            # IndexError: list index out of range
            # KeyError: 'Reservations' 또는 'Instances' 키가 없는 경우
            instance_status = 'Status Not Found'
        print(instance_status)
        
    return JsonResponse({"instanceStatus : instance_status"}, safe=False)   
        
        
        

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
    
    serviceInfo = [model_to_dict(svc) for svc in serviceData]

    
    service_info = []
    service_info_list = []
    
    for service in serviceData: 
        service_info = model_to_dict(service)
        service_info['region_name'] = service.region_no.region_name
        service_info['db_name'] = service.db_no.db_name
        service_info['backend_name'] = service.backend_no.backend_name
        # today = str(service.create_date)
        # service_info['today'] = today
        service_info['create_date'] = str(service.create_date)
    
            
        # 인스턴스 상태 불러오기
        # fixme: 인스턴스 아이디 가져오기!!!!!
        instance_id = 'i-0cde9652658517c13'
        ec2 = boto3.client('ec2')
        # response = ec2.describe_instances(InstanceIds=[instance_id])
        # instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            reservation = response['Reservations'][0]
            instance = reservation['Instances'][0]
            instance_status = instance['State']['Name']
        except (IndexError, KeyError):
            # IndexError: list index out of range
            # KeyError: 'Reservations' 또는 'Instances' 키가 없는 경우
            instance_status = 'Status Not Found'
        
        
        service_info_list.append(service_info)
        service_info_list.append(instance_status)    
    
        # print(instance_status)
        # print(f"Instance ID {instance_id} is in state: {instance_status}")
        
    # json_data = json.dumps(service_info_list)

    return JsonResponse({'serviceInfo' : service_info_list}, safe=False)
    
    #data_to_send = serviceInfo[0]
    # print(json_data)
    
