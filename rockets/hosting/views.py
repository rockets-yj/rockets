from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
import re
from django.http import HttpResponse
import os
import zipfile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def delete_local_media_file(file_path):
    # 로컬 media 경로 설정
    media_root = settings.MEDIA_ROOT

    # 파일의 절대 경로 생성
    absolute_file_path = os.path.join(media_root, file_path)

    try:
        # 파일 삭제
        os.remove(absolute_file_path)
        print(f'파일이 삭제되었습니다: {absolute_file_path}')
        return True
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {absolute_file_path}')
        return False
    except Exception as e:
        print(f'파일 삭제 중 오류 발생: {e}')
        return False


# 삭제할 파일의 상대 경로 (예: 'uploads/example.txt')
file_to_delete = 'test231204.zip'

# 로컬 media 폴더에서 파일 삭제
delete_local_media_file(file_to_delete)


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
def upload_file(request, file, serviceName):
    if file :
        uploaded_file = file
        print("uploaded_file: ", uploaded_file)
        
        # 로컬에 파일 저장
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        # uploaded_file.name : 업로드된 파일의 원래 이름 / 객체에서 'name' 속성으로 가져온 원래 파일 이름
        # uploaded_file: 실제로 업로드된 파일 객체 / 새로운 이름
                        # 이 이름으로 로컬에 저장됨.
        print("filename:", filename)
        
        
        # 압축 해제
        extract_path = os.path.join(fs.location, serviceName)  # 압축을 해제할 경로
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(os.path.join(fs.location, filename), 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # 압축 해제된 파일들의 경로를 반환
        extracted_file_path = os.listdir(extract_path)
        print("extracted_file_path: ", extracted_file_path)
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
        s3_file_path = ""
        
        # 압축 해제한 파일을 모두 포함시키기
        # os.walk() : 지정된 디렉터리 아래에 있는 파일과 디렉터리를 순회하는 함수
        # root : 현재 순회 중인 디렉토리의 경로
        # dirs: 현재 디렉터리에 포함된 서브데릭터리의 리스트
        # files : 해당 디렉터리에 포함된 파일들의 리스트
        for root, dirs, files in os.walk(_extracted_file):
            for file in files:
                local_path = os.path.join(root, file)
                print("for문 안에 local_path: " + local_path)
                # s3_prefix = os.getcwd() + "/media/" + _serviceName + "/"
                s3_prefix = ""
                s3_file_path = os.path.join(s3_prefix, os.path.relpath(local_path, _extracted_file))
                print("s3_file_path: ", s3_file_path)  
                # os.path.relpath(a, b) : 두 경로 사이의 상대 경로를 반환, b를 기준으로 한 a의 상대 경로를 반환
                # a : 파일의 전체 경로
                # b : 기준이 되는 디렉터리의 경로
                

        
                # 로컬 파일 경로 = hosting에서 받은 파일을 여기로 연결 
                # local_file_path = os.getcwd() + "/" + _projectFile
                # local_file_path = os.getcwd() + "/media/" + _serviceName
                local_file_path = os.path.join(_extracted_file, file)
                print("local_file_path: ", local_file_path)  #/home/rocket/git-workspace/leegit/rockets/rockets
            

                s3_create_result = s3_fileupload_def.upload_to_s3(local_file_path, _serviceName, s3_file_path)
                print("s3_create_result: ", s3_create_result)
                # s3_file_url = f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_file_path}'
                
                # 2) S3에 올리면 로컬에 저장한 파일 지우기
                
                result_msg = ""
                if s3_create_result != 1 :
                    result_msg = "파일 업로드 실패"
                    break;
                    
        if not result_msg :
            #todo: s3주소 db에 저장하기
            result_mssg = "호스팅이 성공하였습니다."
            
        return result_msg 


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
        
        print("_projectFile:", _projectFile)
        
        
        print("_serviceName:", _serviceName)
        # 1-2. 세션에 올린 userNo 가져오기
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
        #TODO 
        # 2. 로컬에 파일 저장하기 (settings.py에 media 경로 연결하기)
        if new_record_id != 0:  
            # newfileName = _serviceName
            _extracted_file = upload_file(request, _projectFile, _serviceName)
            print("upload_file result: ", _extracted_file)
            
            if _extracted_file :
                #TODO 
                # 3. S3 생성하기
                # 서비스 이름 가져오기
                result = create_s3(_serviceName, _extracted_file)       
            else :
                result = "S3에 파일 업로드 실패"
                    
        else :
            result = "호스팅에 실패하였습니다."

    return render(request, 'hosting/hostingResult.html', {'result' : result})