from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *


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
        # userNo = request.session.get('UNO')
        userNo = 1
        userData = Userinfo.objects.get(uno=userNo)

        # 해당하는 regionno에 해당하는 값을 가져옴 (한 행을 다 가져옴)
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
        )
        
        service_aws_instance.save()

        new_record_id = service_aws_instance.service_no

        result = ""

        if new_record_id > 0 :
            result = "호스팅이 성공하였습니다."
        else :
            result = "호스팅에 실패하였습니다."

        return render(request, 'hosting/hostingResult.html', {'result' : result})
    