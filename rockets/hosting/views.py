from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.utils import timezone
from s3_functions import *
from datetime import datetime
import re
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import zipfile
from django.core.files.storage import FileSystemStorage
from acm import ACM
from ecr_functions import *
from ECR.views import *
from s3_functions import * 
from try_helm import *
from cloudfront import *  
from hosting.views import *
import time 



session = boto3.Session (
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)


@csrf_exempt
def serviceNameCheck(serviceName):
    # 영문 소문자와 -만 허용하도록 정규표현식 사용
    if not re.match("^[a-z0-9-]+$", serviceName):
        error_message = '서비스 이름은 영문 소문자와 -만 사용 가능합니다.'
        print(error_message)
        #return render(serviceName, 'hosting/hostingPage.html', {'error' : '서비스 이름은 영문 소문자, 숫자, -만 사용 가능합니다.'} )
        return error_message
    #return값 error 프린트하고 hosting 페이지로 돌아가기

    # 숫자만 입력된 경우 처리
    if serviceName.isdigit():
        error_message = '서비스 이름에는 숫자만 입력할 수 없습니다.'
        print(error_message)
        #return render(serviceName, 'hosting/hostingPage.html', {'error' : '서비스 이름에는 숫자만 입력할 수 없습니다.'} )
        return error_message
    #return값 error 프린트하고 hosting 페이지로 돌아가기

    # 소문자로 변경하고 trim 적용 -> 그러면 progressed_service_name을 아래에서 확인해야하나?
    progressed_service_name = serviceName.lower().strip()
    print(progressed_service_name)

    # 여기 DB service_name과 위에proceseed_service_name이 중복되는지 중복값 비교  
    if Serviceaws.objects.filter(service_name=progressed_service_name).exists():
        error_message = '이미 사용중인 서비스 이름입니다.'
        print(error_message)
        #return render(progressed_service_name, 'hosting/hostingPage.html', {'error' : '이미 사용중인 아이디 입니다.'} )
        return error_message
        #return값 error 프린트하고 hosting 페이지로 돌아가기

    else:
        # return 값이 1일 때 아래 userHosting 실행하기
        print("1")
        return True




# Create your views here.
# 호스팅 페이지로 이동
def userhostingPage(request):
    return render(request, 'hosting/hostingPage.html')


# 호스팅 정보 삽입
@csrf_exempt
def userHosting(request):
    
    """
    # html에서 가져올 값
    # 1. 서비스이름
    # 2. 리전
        1 ap-northeast-2 Seoul
        2 ap-northeast-2 Tokyo
    # 3. 백엔드 언어
        1 Python
        2 NodeJS
        3 Spring
    # 4. 프론트 사용여부 (Y/N)
    # 5. 데이터베이스 이름(넘버)
        1 MYSQL
        2 MariaDB
        3 Redis
        4 External 
    # 6. 파일

    """


    if request.method == 'POST' :
        # 1-1. POST 타입으로 넘어온 데이터 받기
        _serviceName = request.POST.get("serviceName")
        _regionNo = request.POST.get("regionNo")
        _backendNo = request.POST.get("backendNo")
        _frontendFl = request.POST.get("frontendFl")
        _dbNo = request.POST.get("dbNo")
        
        # 1-2. 세션에 올린 userNo 가져오기
        # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
        userNo = request.session.get('UNO')
        # userNo = 1

        # 해당하는 regionno에 해당하는 값을 가져옴 (한 행을 다 가져옴)
        userData = Userinfo.objects.get(uno=userNo)
        regionData = Region.objects.get(region_no=_regionNo)
        backendData = BackendLanguage.objects.get(backend_no=_backendNo)
        dbData = DbList.objects.get(db_no=_dbNo)


        # 그 중 원하는 값을 사용할 때
        # regionData.region_name

        # 2.ServiceAws 테이블에 넣기
        service_aws_instance = Serviceaws(
            uno = userData, # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
            region_no = regionData,
            db_no = dbData,
            backend_no = backendData,
            service_name = _serviceName,
            frontend_fl = _frontendFl,
            ecr_uri = None, # 또는 빈 문자열'' 할당 -> Null
            load_balancer_name = None,
            s3_arn = None,
            cloudfront_dns = None,
            create_date=timezone.now()
        )
        print("이제 됨")
        # print(timezone.now())
        # print(service_aws_instance.create_date)
        
        service_aws_instance.save()

        new_record_id = service_aws_instance.service_no
        result = ""

        # DB에 정보 저장에 성공한다면, 
        #TODO 
        # 2. 로컬에 파일 저장하기 (settings.py에 media 경로 연결하기)
        if new_record_id != 0:  
            # newfileName = _serviceName
            _extracted_file = upload_file(_projectFile, _serviceName)
            # print("upload_file result: ", _extracted_file)
            
            if _extracted_file :
                #TODO 
                # 3. S3 생성하기
                result = create_s3(_serviceName, _extracted_file) 
                
                if result == 1 : 
                    result = "호스팅 성공"
                    print('S3 업로드 완료')
                
                else :
                    result = "호스팅 실패"
            
            else :
                result = "S3 생성 실패"
                
    return True


@csrf_exempt
def all_in_one(request):
    _service_name = request.POST.get('serviceName')
    _service_name = str(_service_name).lower()
    RegionNo = request.POST.get('regionNo')
    result = ''
    # ecr 생성    
    try:
        service_check = serviceNameCheck(_service_name)
        if service_check is True :
            pass
        else :
            return render(request, 'hosting/hostingPage.html', { 'error' : service_check})
        
        userHosting(request)
        
        _service = Serviceaws.objects.get(service_name=_service_name)
        print(_service.region_no.region_no, type(_service.region_no.region_no))
        _region_no = int(_service.region_no.region_no)
        region =  Region.objects.get(region_no=_region_no)   
        print(region)  
        
        time.sleep(450)
        # _service.ecr_uri = create_ecr_and_push_image(_service_name, region.region_code)
        # _service.save()
        
        # try_helm.delete_folder(_service_name)
        # try_helm.create_service(_service_name, _service.ecr_uri, _service.port, _service_name)
        # try_helm.create_eks_nodegroup(_service_name, _service_name, 'eks-rockets')
        
        
        # try_helm.helm_start(_service_name)
        # time.sleep(10)                                   # 바로 LB 못 불러와서 잠시 후 불러오기 위해서
        # _service.load_balancer_name = try_helm.get_load_balancer_dns(_service_name)
        # _service.save()     
        # _service.cloudfront_dns = cf_create.create_cloudfront_distribution(_service_name,_service.load_balancer_name)
        # _service.save()
        
        
        # _service.domain=addDomain(_service_name, _service.cloudfront_dns)
        # _service.save()
        
        
        result = "호스팅에 성공하였습니다."
        return render(request, 'hosting/hostingResult.html', {'result' : result, 'dns' : _service.domain})
    
    except Exception as e :
        # 에러 발생 시 로딩 프로세스 업데이트
        return render (request,'hosting/hostingResult.html', {'result': f' 에러: {e}'})


'''
    # 파일 업로드 완료 (20초)
    # 도커 이미지 업로드 완료 (20초)
    # 노드 생성 완료 (4분)
    # cloudfront 생성 완료 (2분 30초)
    # 도메인 할당 완료 (20초)
'''