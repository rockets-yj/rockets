import boto3
import os

# AWS 환경변수 session으로 가져오기 
session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name= os.environ.get('REGION')
)

aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
region_name = session.region_name


# 버킷 안에 모든 데이터를 삭제해야 버킷 삭제가 가능함
# 버킷 안 데이터 삭제 하는 함수 delete_all_objects_in_bucket
def delete_all_objects_in_bucket(bucket_name):
    # boto3 S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    try:
        # 버킷 안의 객체 목록 가져오기
        response = s3.list_objects_v2(Bucket=bucket_name)

        # 버킷 안의 모든 객체(파일, 디렉토리, zip파일 등) 전체 삭제 후 결과 print
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Object '{obj['Key']}' deleted from bucket '{bucket_name}'")

        print(f"All objects deleted from bucket '{bucket_name}'")
    except Exception as e:
        print(f"Error deleting objects from bucket '{bucket_name}': {e}")

# 버킷 삭제하는 함수 delete_all_objects_in_bucket를 받아와서 쓰기 때문에 위 코드랑 같이 사용해야 함 
def delete_s3_bucket(bucket_name):
    # boto3 S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    try:
        # 버킷 안의 모든 객체 삭제
        delete_all_objects_in_bucket(bucket_name)

        # S3 버킷 삭제
        s3.delete_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting S3 bucket '{bucket_name}': {e}")


# 삭제할 bucket name을 여기에 변수로 선언하기 -> DB와 연결필요
delete_bucket_name = "upload8.rockets-yj.com"

# 함수 실행하기
delete_s3_bucket(delete_bucket_name)
