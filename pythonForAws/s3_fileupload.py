import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    # AWS 계정 정보 설정
    aws_access_key_id = 'AKIAY4FU3OUXBF7JOCX3'
    aws_secret_access_key = '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'
    aws_region = 'ap-northeast-2'

    # Boto3 S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

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
    # 로컬 파일 경로
    local_file_path = 'local-file.txt'
    
    # S3 버킷 이름
    bucket_name = 'your-s3-bucket-name'

    # S3 파일 경로
    s3_file_path = 'path-in-bucket/local-file.txt'

    # 파일 업로드 및 S3 주소 가져오기
    s3_file_url = upload_to_s3(local_file_path, bucket_name, s3_file_path)

    if s3_file_url:
        print(f'파일이 업로드되었습니다. S3 주소: {s3_file_url}')


#aws s3 presign s3://rockets-yj/testsong/test.txt : test.txt 파일 가져오기 