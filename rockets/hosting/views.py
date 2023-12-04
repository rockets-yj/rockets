from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from django.utils import timezone
from s3_functions import *
from datetime import datetime
import re
from django.http import HttpResponse

# Create your views here.
# 호스팅 페이지로 이동
def userhostingPage(request):
    return render(request, 'hosting/hostingPage.html')


# # 서비스이름 가져오기
# def getServiceName(request):
#     userNo = request.session.get('UNO');
    
#     serviceName = (
#         Serviceaws.objects.filter(userNo=userNo).values('serviceName').first()
#     )
    
#     return serviceName



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
        _port = request.POST.get("portNumber")
        _projectFile = request.FILES.get("projectFile")
        
        print("_serviceName:", _serviceName)
        # 1-2. 세션에 올린 userNo 가져오기
        # fixme: 로그인 기능 완성되면 세션에서 가져오는 걸로 바꾸기
        userNo = request.session.get('UNO')
        # userNo = 1
        
        # 정규식, lower, trim 써서 정규식에 맞는지 한번 더 확인

        # 해당하는 regionno에 해당하는 값을 가져옴 (한 행을 다 가져옴)
        userData = Userinfo.objects.get(uno=userNo)
        regionData = Region.objects.get(region_no=_regionNo)
        backendData = BackendLanguage.objects.get(backend_no=_backendNo)
        dbData = DbList.objects.get(db_no=_dbNo)


        # 그 중 원하는 값을 사용할 때
        # now_naive = datetime.now()
        # now_aware = timezone.make_aware(now_naive, timezone=timezone.get_current_timezone())
        # timezone.activate(timezone.get_current_timezone())
        # now_localized = timezone.localtime(now_aware)
        
        # regionData.region_name
        # now = timezone.now()
        # korea_time = timezone.localtime(now, timezone=timezone.get_current_timezone())
        # print(korea_time)

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
            # create_date=now_localized 
            create_date=timezone.now(),
            port=_port,
        )
        # print(timezone.now())
        # print(service_aws_instance.create_date)
        
        service_aws_instance.save()

        new_record_id = service_aws_instance.service_no
        print("new_record_id: ", new_record_id)
        
        result = ""

        # DB에 정보 저장에 성공한다면, 
        if new_record_id != 0:  
            # 서비스 이름 가져오기
            print("userNo: ", userNo)
            print("serviceName: ", _serviceName)

            try:
                # S3 생성 함수 갖고 오기
                s3Result = s3_bucket_create_def.create_s3_bucket(_serviceName)
                print("버킷 생성 성공 s3Result: ", s3Result)
                
            except Exception as e:
                print(f's3 생성 중 에러 발생: {e}')

            # 성공하면 1 return
            if s3Result == 1 :
                # S3에 파일을 업로드하는 함수 갖고오기
                bucket_name = _serviceName
                s3_file_path = _serviceName
            
                s3_file_url = s3_fileupload_def.upload_to_s3(_projectFile, bucket_name, s3_file_path)
                print("_projectFile: ", _projectFile)
                print("s3_file_url: ", s3_file_url)
                # s3_file_url = f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_file_path}'
            
                
                # 성공하면
                if s3_file_url :
                    #todo: s3주소 저장하기
                    result = "호스팅이 성공하였습니다."
                
                else :
                    result = "파일 업로드 실패"
                    
        else :
            result = "호스팅에 실패하였습니다."

    return render(request, 'hosting/hostingResult.html', {'result' : result})