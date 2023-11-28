from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

#views에서 유저 선택시 유저정보 가져오는 화면

# Admin 서비스 전체 목록 조회
@csrf_exempt
def adminService(request):
    
    serviceList = (
        Serviceaws.objects
        .all()
        .prefetch_related('backend_no', 'region_no', 'db_no')
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
    
    json_data = json.dumps(service_info_list, default=str)
    
    return render(request, 'rocket-admin/adminService.html', {'svcList' : json_data})



# Admin 서비스 하나 상세 조회
@csrf_exempt
def adminServiceInfo(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        serviceListId = data.get('serviceListId',None)

        print("serviceID:",serviceListId)
        
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