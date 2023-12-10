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

def delete_route53_record(zone_id, record_name, record_type, record_value):
    # AWS 자격 증명 및 Route 53 클라이언트 생성
    aws_access_key = aws_access_key_id
    aws_secret_key = aws_secret_access_key
    client = boto3.client('route53', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    # 레코드를 삭제할 호스트 존 ID, 레코드 이름, 레코드 타입 및 레코드 값
    hosted_zone_id = zone_id
    record_set_name = record_name
    record_set_type = record_type
    record_set_value = record_value

    try:
        # Route 53 레코드 삭제 요청
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': record_set_name,
                            'Type': record_set_type,
                            'TTL': 300,  # TTL 값 설정 (원하는 값으로 변경)
                            'ResourceRecords': [
                                {
                                    'Value': record_set_value
                                }
                            ]
                        }
                    }
                ]
            }
        )

        # 삭제 요청에 대한 응답 확인
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"Route 53 record '{record_set_name}' of type '{record_set_type}' deleted successfully.")
        else:
            print(f"Failed to delete Route 53 record. Response: {response}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# 레코드를 삭제할 호스트 존 ID, 레코드 이름, 레코드 타입 및 레코드 값 지정
zone_id_to_delete = 'Z0958311YBP9BJL383S5'
record_name_to_delete = '_6711f6d4853b8180a57dc30edc42066c.youngtesttest12345.rockets-yj.com'
record_type_to_delete = 'CNAME'
record_value_to_delete = '_3053fe9aa9cdad3f1532beb29cac1f57.mhbtsbpdnt.acm-validations.aws.'

# 함수 호출로 레코드 삭제
delete_route53_record(zone_id_to_delete, record_name_to_delete, record_type_to_delete, record_value_to_delete)