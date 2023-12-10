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

    # 소문자로 변경하고 trim 적용 -> 그러면 processed_service_name을 아래에서 확인해야하나?
    processed_service_name = serviceName.lower().strip()
    print(processed_service_name)

    # 여기 DB service_name과 위에proceseed_service_name이 중복되는지 중복값 비교  
    if Serviceaws.objects.filter(service_name=processed_service_name).exists():
        error_message = '이미 사용중인 서비스 이름입니다.'
        print(error_message)
        #return render(processed_service_name, 'hosting/hostingPage.html', {'error' : '이미 사용중인 아이디 입니다.'} )
        return error_message
        #return값 error 프린트하고 hosting 페이지로 돌아가기

    else:
        # return 값이 1일 때 아래 userHosting 실행하기
        print("1")
        return True



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

    # 소문자로 변경하고 trim 적용 -> 그러면 processed_service_name을 아래에서 확인해야하나?
    processed_service_name = serviceName.lower().strip()
    print(processed_service_name)

    # 여기 DB service_name과 위에proceseed_service_name이 중복되는지 중복값 비교  
    if Serviceaws.objects.filter(service_name=processed_service_name).exists():
        error_message = '이미 사용중인 서비스 이름입니다.'
        print(error_message)
        #return render(processed_service_name, 'hosting/hostingPage.html', {'error' : '이미 사용중인 아이디 입니다.'} )
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
        print("fs.location:", fs.location)
        extract_path = os.path.join(fs.location, serviceName)  # 압축을 해제할 경로
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(os.path.join(fs.location, filename), 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # 압축 해제된 파일들의 경로를 반환
        extracted_file_path = os.listdir(extract_path)
        # print("extracted_file_path: ", extracted_file_path)
        return extracted_file_path
        
    # return None

def addDomain(service_name,cloud_front):
    # Route 53 클라이언트를 생성합니다.
    client = session.client('route53')
    print(f'{service_name} : {cloud_front}')
    # 도메인에 레코드를 생성
    domain_name = 'rockets-yj.com'

    # 도메인 id 확인
    response = client.list_hosted_zones_by_name() # 모든 hosted Zone 을 가져옴
    hosted_zone_id = None

    for hosted_zone in response['HostedZones']:
        if hosted_zone['Name'] == domain_name + '.' :
            hosted_zone_id = hosted_zone['Id']
            break
        
    # /hostedzone/Z0958311YBP9BJL383S5 이런식으로 반환을 하기 때문에 앞의 /hostedzone/ 을 삭제한다
    hosted_zone_id = hosted_zone_id.split("/hostedzone/")[1]
    print(hosted_zone_id)

    # 로드밸런서의 주소
    cloud_front_dns = cloud_front

    response = client.change_resource_record_sets(
        HostedZoneId = hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': f'www.{service_name}.rockets-yj.com', # 원하는 도메인 이름
                        'Type': 'CNAME', # ipv4 주소는 A, dns 는 CNAME ,
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': cloud_front_dns
                            },
                        ],
                    }
                },
            ]
        }
    )
    return f'www.{service_name}.rockets-yj.com'




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
        
        if s3_create_result == 1 :
            return 1
        
        else :            
            return 0
            

    
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
# 호스팅 정보 삽입
@csrf_exempt
def userHosting(request):


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
        
        #정규식, lower, trim 써서 정규식에 맞는지 한번 더 확인




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
        
        _service.ecr_uri = create_ecr_and_push_image(_service_name, region.region_code)
        _service.save()
        
        try_helm.delete_folder(_service_name)
        try_helm.create_service(_service_name, _service.ecr_uri, _service.port, _service_name)
        try_helm.create_eks_nodegroup(_service_name, _service_name, 'eks-rockets')
        try_helm.helm_start(_service_name)
        time.sleep(10)                                   # 바로 LB 못 불러와서 잠시 후 불러오기 위해서
        _service.load_balancer_name = try_helm.get_load_balancer_dns(_service_name)
        _service.save()
        _service.cloudfront_dns = cf_create.create_cloudfront_distribution(_service_name,_service.load_balancer_name)
        _service.save()
        _service.domain=addDomain(_service_name, _service.cloudfront_dns)
        _service.save()
        result = "호스팅에 성공하였습니다."
        
        return render(request, 'hosting/hostingResult.html', {'result' : result, 'dns' : _service.domain})
    except Exception as e :
        return render (request,'hosting/hostingResult.html', {'result': f' 에러: {e}'})
    