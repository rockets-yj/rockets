import boto3
import mimetypes
import os
from botocore.exceptions import NoCredentialsError
from django.core.files import File

#AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('AWS_REGION')
)

aws_region = os.environ.get('AWS_REGION')


def upload_to_s3(local_folder_path, bucket_name):

    '''
    local_file_path : 로컬에서 저장되는 경로
    bukcet_name : 버킷이름 ( name.rockets-yj.com 형식)
    s3_file_path : S3 버킷 안에 저장되는 경로
    '''
    service_name = bucket_name
    local_folder_path = 'media/' + bucket_name #bucket_name 자체는  = serviceName
    # local_folder_path = 'media/' 
    MAIN_DOMAIN = ".rockets-yj.com" 
    bucket_name = bucket_name + MAIN_DOMAIN
    
    # Boto3 S3 클라이언트 생성
    s3 = session.client('s3')
    
    try:
        # 로컬 폴더의 파일 목록 가져오기
        for root, dirs, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                # s3_key = f'{service_name}/{os.path.relpath(local_file_path, local_folder_path)}'
                s3_key = f'{os.path.relpath(local_file_path, local_folder_path)}'
                
                # 파일 확장자를 가져오기
                _, file_extension = os.path.splitext(local_file_path)
            
                # ContentType을 결정하기 위해 파일 확장자를 기반으로 MIME 타입을 가져오기
                content_type, _ = mimetypes.guess_type(local_file_path)
                
                # 파일이 인식되지 않는 경우 기본값으로 'application/octet-stream' 사용
                if not content_type:
                    content_type = 'application/octet-stream'
            
                # ContentType 메타데이터 설정
                extra_args = {'ContentType': content_type}
                
                # S3에 업로드
                s3.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs=extra_args)
        
        return 1
        
            
        # 업로드된 파일의 S3 주소 생성
        # s3_file_url = f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_file_path}'

    except Exception as e:
        print(f'업로드 중 에러 발생: {e}')
        return None

# if __name__ == '__main__':
#     # 로컬 파일 경로 = hosting에서 받은 파일을 여기로 연결 
#     local_file_path = '/home/rocket/git-workspace/songgit/rockets/rockets/s3_functions/s3_upload_test.txt'
    
#     # S3 버킷 이름 = 서비스이름으로 받아서 저장하기 
#     bucket_name = 'rockets-yj'

#     # S3 파일 경로: 위 s3 버킷 안에 폴더로 생성함
#     # 아래 rockets라는 폴더를 자동으로 생성하고 안에 파일을 저장함
#     s3_file_path = 'rockets/s3_upload_test.txt'

#     # 파일 업로드 및 S3 주소 가져오기
#     s3_file_url = upload_to_s3(local_file_path, bucket_name, s3_file_path)

#     if s3_file_url:
#         print(f'파일이 업로드되었습니다. S3 주소: {s3_file_url}')

#같은 파일명으로 재실행시 덮어쓰기
#test.txt 파일 경로 가져오는 명령어: aws s3 presign s3://rockets-yj/testsong/test.txt