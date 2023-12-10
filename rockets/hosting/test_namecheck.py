from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.utils import timezone
from s3_functions import *
from datetime import datetime
import re
from django.http import HttpResponse
import os
import zipfile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404

@csrf_exempt
def serviceNameCheck(serviceName):
    # 영문 소문자와 -만 허용하도록 정규표현식 사용
    if not re.match("^[a-z0-9-]+$", serviceName):
        error_message = '서비스 이름은 영문 소문자와 -만 사용 가능합니다.'
        print(error_message)
        return render(serviceName, 'hosting/hostingPage.html', {'error' : '서비스 이름은 영문 소문자, 숫자, -만 사용 가능합니다.'} )
    #return값 error 프린트하고 hosting 페이지로 돌아가기

    # 숫자만 입력된 경우 처리
    if serviceName.isdigit():
        error_message = '서비스 이름에는 숫자만 입력할 수 없습니다.'
        print(error_message)
        return render(serviceName, 'hosting/hostingPage.html', {'error' : '서비스 이름에는 숫자만 입력할 수 없습니다.'} )
    #return값 error 프린트하고 hosting 페이지로 돌아가기

    # 소문자로 변경하고 trim 적용 -> 그러면 processed_service_name을 아래에서 확인해야하나?
    processed_service_name = serviceName.lower().strip()
    print(processed_service_name)

    # 여기 DB service_name과 위에proceseed_service_name이 중복되는지 중복값 비교  
    if Serviceaws.objects.filter(service_name=processed_service_name).exists():
        error_message = '이미 사용중인 서비스 이름입니다.'
        print(error_message)
        return render(processed_service_name, 'hosting/hostingPage.html', {'error' : '이미 사용중인 아이디 입니다.'} )
        #return값 error 프린트하고 hosting 페이지로 돌아가기

    else:
        # return 값이 1일 때 아래 userHosting 실행하기
        print("1")
        return userHosting