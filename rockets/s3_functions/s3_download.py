import boto3
import os
from botocore.exceptions import NoCredentialsError

session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('AWS_REGION')
)

aws_region = os.environ.get('AWS_REGION')

def download_from_s3(bucket_name, s3_file_path, local_file_path):

    # Boto3 S3 클라이언트 생성
    s3 = session.client('s3')

    try:
        # S3 버킷에서 파일 다운로드
        s3.download_file(bucket_name, s3_file_path, local_file_path)

        print(f'파일이 다운로드되었습니다. 로컬 경로: {local_file_path}')

    except NoCredentialsError:
        print('AWS 계정 정보가 정확한지 확인하세요.')
    except Exception as e:
        print(f'파일 다운로드 중 오류 발생: {e}')

if __name__ == '__main__':
    # S3 버킷 이름
    bucket_name = 'rockets-yj'

    # S3 파일 경로
    s3_file_path = 'rockets/s3_upload_test.txt'

    # 로컬에 저장할 파일 경로
    local_file_path = '/home/rocket/git-workspace/songgit/rockets/rockets/s3_functions/s3_download_test.txt'

    # 파일 다운로드
    download_from_s3(bucket_name, s3_file_path, local_file_path)
