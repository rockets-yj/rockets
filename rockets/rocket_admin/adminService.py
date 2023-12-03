from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.shortcuts import render

#views에서 유저 선택시 유저정보 가져오는 화면

# optimize: Admin 서비스 목록 
# Admin 서비스 전체 목록 조회
@csrf_exempt
def adminService(request):
    
    serviceList = (
        Serviceaws.objects
        .all()
        .prefetch_related('backend_no', 'region_no', 'db_no', 'uno')
    )
    
    service_info = []
    service_info_list = []
    
    for service in serviceList: 
        service_info = model_to_dict(service)
        service_info['region_name'] = service.region_no.region_name
        service_info['db_name'] = service.db_no.db_name
        service_info['backend_name'] = service.backend_no.backend_name
        service_info['user_name'] = service.uno.uname
        service_info['create_date'] = service.create_date
        
        service_info_list.append(service_info)
    
    # print(service_info_list)
    json_data = json.dumps(service_info_list, default=str)
    
    return render(request, 'rocket-admin/adminService.html', {'svcList' : json_data})



# Admin 서비스 하나 상세 조회
@csrf_exempt
def adminServiceInfo(request):
    userNo = request.session.get('UNO')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        serviceListId = data.get('serviceListId',None)

        # print("serviceID:",serviceListId)
        
        serviceData = (
            Serviceaws.objects
            .filter(service_no = serviceListId)
            .prefetch_related('backend_no', 'region_no', 'db_no', 'uno')
        )
        
        service_info = []
        
        for service in serviceData: 
            service_info = model_to_dict(service)
            service_info['region_name'] = service.region_no.region_name
            service_info['db_name'] = service.db_no.db_name
            service_info['backend_name'] = service.backend_no.backend_name
            service_info['user_name'] = service.uno.uname
            service_info['create_date'] = service.create_date
            
        json_data = json.dumps(service_info, default=str)
        return JsonResponse({'serviceInfo': json_data})  # 수정: JsonResponse으로 변경
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'})
    # return render(request, 'rocket-admin/adminService.html', {'serviceInfo' : json_data})
    
# -------------------------------------


# optimize: 회원의 서비스 정보 조회
@csrf_exempt
def adminUserService(request):
    
    userNo = request.GET.get('uno')
    # print("userNo : ", userNo)
    
    serviceList = (
        Serviceaws.objects
        .filter(uno=userNo)
        .prefetch_related('backend_no', 'region_no', 'db_no', 'uno')
    )
    
    # print(f"serviceList : {serviceList}")   
    
    service_info = []
    service_info_list = []
    
    for service in serviceList: 
        service_info = model_to_dict(service)
        service_info['region_name'] = service.region_no.region_name
        service_info['db_name'] = service.db_no.db_name
        service_info['backend_name'] = service.backend_no.backend_name
        service_info['user_name'] = service.uno.uname
        service_info['user_id'] = service.uno.uid
        service_info['create_date'] = service.create_date
        
        service_info_list.append(service_info)
    
    # print(service_info_list)
    json_data = json.dumps(service_info_list, default=str)
    
    return render(request, 'rocket-admin/adminUserService.html', {'svcList' : json_data})
    
    
    # return render(request, 'rocket-admin/adminUserService.html', {'serviceList' : service_info_list})
    # return JsonResponse({'serviceList': json_data}) 
    
    
# optimize: 회원의 서비스 상세 정보

#     # todo: fetch로 serviceId를 가져와서, 
#     # todo: 해당 서비스의 정보를 다 가져오고
#     # todo: html 페이지로 넘기고(render) json 파일로 넘기고
#     # todo: 그 html에 js 파일 넣고
#     # todo: 그 js에서 처리하자
@csrf_exempt
def adminUserServiceInfo(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        serviceListId = data.get('serviceListId',None)

        print("serviceID:", serviceListId)
        
        serviceData = (
            Serviceaws.objects
            .filter(service_no = serviceListId)
            .prefetch_related('backend_no', 'region_no', 'db_no', 'uno')
        )
        
        service_info = []
        
        for service in serviceData: 
            service_info = model_to_dict(service)
            service_info['region_name'] = service.region_no.region_name
            service_info['db_name'] = service.db_no.db_name
            service_info['backend_name'] = service.backend_no.backend_name
            service_info['user_name'] = service.uno.uname
            service_info['create_date'] = service.create_date
            
        json_data = json.dumps(service_info, default=str)
        
        
        return JsonResponse({'serviceInfo': json_data})  # 수정: JsonResponse으로 변경
        # return render(request, 'rocket-admin/adminUserServiceInfo.html', {'svcList' : json_data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'})
    # return render(request, 'rocket-admin/adminService.html', {'serviceInfo' : json_data})
