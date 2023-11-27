from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict


# Create your views here.
# 사용자 서비스 상태 조회 페이지로 이동
# def userStatusPage(request):
#     return render(request, 'userStatus/userStatus.html')

# 사용자 서비스 조회하기
@csrf_exempt
def viewServiceList(request):
    # 1. userNo를 받아와서 해당 사용자의 서비스 목록 조회하기
    # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
    # userNo = request.session.get('UNO')
    userNo = 1
    
    serviceList = (
        Serviceaws.objects
        .filter(uno=userNo)
        .prefetch_related('backend_no', 'region_no', 'db_no')
    )
    

    
    return render(request, 'userStatus/userStatus.html', {'serviceList' : serviceList})
    

# 사용자 서비스 조회-js
@csrf_exempt
def viewServiceListJs(request):
    # 1. userNo를 받아와서 해당 사용자의 서비스 목록 조회하기
    # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
    # userNo = request.session.get('UNO')
    userNo = 1
    
    serviceList = (
        Serviceaws.objects
        .filter(uno=userNo)
        .prefetch_related('backend_no', 'region_no', 'db_no')
    )
    
    
    
    context = {
        "serviceList" : serviceList,
        "serviceList_js" : json.dumps([srv.json() for srv in serviceList])
    }
    
    return render(request, 'userStatus/userStatus.html', context)
    
    
#사용자 서비스 상세 조회 - js. ajax.
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
    print(serviceData)
    
    serviceInfo = [model_to_dict(srv) for srv in serviceData]

    #serviceInfo = list(serviceData)
    
    print("aaaaaaaaaaaa",serviceInfo)
    
    service_info = []
    
    
    for service in serviceData: 
        service_info = model_to_dict(service)
        service_info['region_name'] = service.region_no.region_name
        service_info['db_name'] = service.db_no.db_name
        service_info['backend_name'] = service.backend_no.backend_name
        today = str(service.create_date)
        service_info['today'] = today
            
    #data_to_send = serviceInfo[0]
    json_data = json.dumps(service_info)
    print(json_data)
    
    return JsonResponse({'serviceInfo' : json_data})



# @csrf_exempt
# def viewServiceInfo(request):
#     if request.method == 'POST':
#         # POST 요청에서 JSON 데이터 추출
        
#         data = json.loads(request.body.decode('utf-8'))
#         serviceListId = data.get('serviceListId')
        
#         print(serviceListId)
        
#         # 사용자의 서비스 하나를 조회
#         serviceData = (
#             Serviceaws.objects
#             .filter(service_no=serviceListId)
#             .prefetch_related('backend_no', 'region_no', 'db_no')
#         )

#         serviceInfo = list(serviceData)
#         return JsonResponse({'serviceInfo': serviceInfo})
#     else:
#         # POST 요청이 아닌 경우 에러 응답
#         return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
