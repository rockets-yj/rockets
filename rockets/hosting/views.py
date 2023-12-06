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


# 파일을 로컬에 저장
def upload_file(file, serviceName):
    if file :
        uploaded_file = file
        # print("uploaded_file: ", uploaded_file)
        
        # 로컬에 파일 저장
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        # uploaded_file.name : 업로드된 파일의 원래 이름 / 객체에서 'name' 속성으로 가져온 원래 파일 이름
        # uploaded_file: 실제로 업로드된 파일 객체 / 새로운 이름
                        # 이 이름으로 로컬에 저장됨.
        # print("filename:", filename)
        
        # fixme: 압축 파일 없을 때 처리하기
        # 압축 해제
        extract_path = os.path.join(fs.location, serviceName)  # 압축을 해제할 경로
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(os.path.join(fs.location, filename), 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # 압축 해제된 파일들의 경로를 반환
        extracted_file_path = os.listdir(extract_path)
        # print("extracted_file_path: ", extracted_file_path)
        return extracted_file_path
        
    # return None


# s3 생성 함수
def create_s3(_serviceName, _extracted_file):
    
    try:
        #3-1 S3 버킷 생성하기
        s3Result = s3_bucket_create_def.create_s3_bucket(_serviceName)
        print("버킷 생성 성공 s3Result: ", s3Result)
        
    except Exception as e:
        print(f's3 생성 중 에러 발생: {e}')
        return "버킷 생성 실패"

    # 성공하면 1 반환
    if s3Result == 1 :
        # 3-2 S3에 파일 업로드하기
        # 1) 로컬에 저장한 파일을 S3에 올리기
        # 폴더로 올리기!!
        
        local_folder_path = ""
        s3_create_result = s3_fileupload_def.upload_to_s3(local_folder_path, _serviceName)
        # print("s3_create_result: ", s3_create_result)
        # s3_file_url = f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_file_path}'
        
        # 2) S3에 올리면 로컬에 저장한 파일 지우기
        # TODO -> 함수 따로 만들어서 ECR 뒤에 실행
        
        result = ""
        if s3_create_result == 1 :
            return 1
        
        else :            
            return 0
            
    


# 호스팅 정보 삽입
@csrf_exempt
def userHosting(request):
    
    """ html에서 가져올 값
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
        # TODO
        # 1. 사용자가 입력한 데이터 저장하기
        # 1-1. POST 타입으로 넘어온 데이터 받기
        _serviceName = request.POST.get("serviceName")
        _regionNo = request.POST.get("regionNo")
        _backendNo = request.POST.get("backendNo")
        _frontendFl = request.POST.get("frontendFl")
        _dbNo = request.POST.get("dbNo")
        _port = request.POST.get("portNumber")
        _projectFile = request.FILES["projectFile"]
        
        # print("_projectFile:", _projectFile)
        # print("_serviceName:", _serviceName)
        
        
        # 1-2. 세션에 올린 userNo 가져오기
        userNo = request.session.get('UNO')
        # userNo = 1
        
        # 정규식, lower, trim 써서 정규식에 맞는지 한번 더 확인

        # 해당하는 regionno에 해당하는 값을 가져옴 (한 행을 다 가져옴)
        userData = Userinfo.objects.get(uno=userNo)
        regionData = Region.objects.get(region_no=_regionNo)
        backendData = BackendLanguage.objects.get(backend_no=_backendNo)
        dbData = DbList.objects.get(db_no=_dbNo)

        # 1-3.ServiceAws 테이블에 넣기
        service_aws_instance = Serviceaws(
            uno = userData, 
            region_no = regionData,
            db_no = dbData,
            backend_no = backendData,
            service_name = _serviceName,
            frontend_fl = _frontendFl,
            ecr_uri = None, # 또는 빈 문자열'' 할당 -> Null 
            load_balancer_name = None, 
            s3_arn = "arn:aws:s3:::" + _serviceName + ".rockets-yj.com", 
            cloudfront_dns = None, 
            # create_date=now_localized 
            create_date=timezone.now(),
            port=_port,
        )
        # print(timezone.now())
        # print(service_aws_instance.create_date)
        
        service_aws_instance.save()

        new_record_id = service_aws_instance.service_no
        # print("new_record_id: ", new_record_id)
        
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
                    result = "호스팅에 성공하였습니다."
                    print('파일 업로드 완료')
                
                else :
                    result = "호스팅에 실패하였습니다."
            
            else :
                result = ""
                
        # 4. DB에 S3 주소 저장하기        
        # if result == 1 :
        #     '''
        #     # s3 arn 주소 형식: arn:aws:s3:::your-bucket-name/your-object-key
        #     # ex) arn:aws:s3:::1206zipfinal.rockets-yj.com
        #     '''
        #     s3_arn_addr = "arn:aws:s3:::" + _serviceName + ".rockets-yj.com"
            
        #     # 원하는 ServiceAws 인스턴스를 가져오기
        #     service_instance = get_object_or_404(Serviceaws, service_no=userData.uno)

        #     # 새로운 S3 ARN 값을 설정
        #     service_instance.s3_arn = s3_arn_addr

        #     # 변경사항을 저장
        #     service_instance.save()
            
        #     result = "호스팅에 성공하였습니다."
                                
                
    return render(request, 'hosting/hostingResult.html', {'result' : result})