from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.core.serializers import serialize
from django.http import JsonResponse

# Create your views here.
# 사용자 서비스 상태 조회 페이지로 이동
# def userStatusPage(request):
#     return render(request, 'userStatus/userStatus.html')

# 사용사 서비스 조회하기
@csrf_exempt
def viewServiceList(request):
    # 1. userNo를 받아와서 해당 사용자의 서비스 목록 조회하기
    # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
    # userNo = request.session.get('UNO')
    userNo = 1
    # serviceList = {
    #     "serviceList" : Serviceaws.objects.filter(uno=userNo) #filter: 모든 레코드
    # }
    
    service_list = list(Serviceaws.objects.filter(uno=userNo)) 
    serialized_data = serialize('json', service_list)

    # serviceList = list(Serviceaws.objects.filter(uno=userNo))  #filter: 모든 레코드
    # serviceListJson = serialize('json', serviceList)
    
    return render(request, 'userStatus/userStatus.html', {'serviceList' : serialized_data})
    
    
    
    
    