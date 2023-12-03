import boto3
import os
from botocore.exceptions import NoCredentialsError

#AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('AWS_REGION')
)

aws_region = os.environ.get('AWS_REGION')


def upload_to_s3(local_file_path, bucket_name, s3_file_path):

    # Boto3 S3 클라이언트 생성
    s3 = session.client('s3')

    try:
        # 로컬 파일을 S3 버킷에 업로드
        s3.upload_file(local_file_path, bucket_name, s3_file_path)

        # 업로드된 파일의 S3 주소 생성
        s3_file_url = f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_file_path}'

        return s3_file_url

    except NoCredentialsError:
        print('AWS 계정 정보가 정확한지 확인하세요.')
        return None

if __name__ == '__main__':
    # 로컬 파일 경로 = hosting에서 받은 파일을 여기로 연결 
    local_file_path = '/home/rocket/git-workspace/songgit/rockets/rockets/s3_functions/s3_upload_test.txt'
    
    # S3 버킷 이름 = 서비스이름으로 받아서 저장하기 
    bucket_name = 'rockets-yj'

    # S3 파일 경로: 위 s3 버킷 안에 폴더로 생성함
    # 아래 rockets라는 폴더를 자동으로 생성하고 안에 파일을 저장함
    s3_file_path = 'rockets/s3_upload_test.txt'

    # 파일 업로드 및 S3 주소 가져오기
    s3_file_url = upload_to_s3(local_file_path, bucket_name, s3_file_path)

    if s3_file_url:
        print(f'파일이 업로드되었습니다. S3 주소: {s3_file_url}')

#같은 파일명으로 재실행시 덮어쓰기
#test.txt 파일 경로 가져오는 명령어: aws s3 presign s3://rockets-yj/testsong/test.txt