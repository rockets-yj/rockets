from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.utils import timezone
from s3_functions import *
from datetime import datetime
import re
from django.http import HttpResponse

@csrf_exempt
def serviceNameCheck(service_name):
    # 영문 소문자와 -만 허용하도록 정규표현식 사용
    if not re.match("^[a-z-]+$", service_name):
        error_message = '서비스 이름은 영문 소문자와 -만 사용 가능합니다.'
        return error_message

    # 소문자로 변경하고 trim 적용
    processed_service_name = service_name.lower().strip()

    # 여기 processed_service_name db와 연결한 네임으로 변경해야함  
    if Serviceaws.objects.filter(service_name=processed_service_name).exists():
        error_message = '이미 사용중인 서비스 이름입니다.'
        return error_message
    else:
        # return 값이 1일 때 아래 userHosting 실행하기 
        return 1
    
result = serviceNameCheck('yangjutest')
print(result)