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


def get_route53_record_value(zone_id, record_name, record_type):
    # AWS 자격 증명 및 Route 53 클라이언트 생성
    aws_access_key = aws_access_key_id
    aws_secret_key = aws_secret_access_key
    client = boto3.client('route53', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    try:
        # Route 53 레코드 조회 요청
        response = client.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        # 조회된 레코드 세트에서 특정 레코드 찾기
        for record_set in response['ResourceRecordSets']:
            if record_set['Name'] == record_name and record_set['Type'] == record_type:
                # CNAME 레코드의 경우 값을 출력
                if record_type == 'CNAME':
                    print(f"Route 53 record '{record_name}' of type '{record_type}' has value: {record_set.get('ResourceRecords', [])}")

                # 다른 레코드 타입의 경우 여러 값이 있을 수 있으므로 값을 출력하지 않음
                else:
                    print(f"Route 53 record '{record_name}' of type '{record_type}' found, but value output is not implemented for this record type.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# 조회할 호스트 존 ID, 레코드 이름 및 레코드 타입 지정
zone_id_to_query = 'Z0958311YBP9BJL383S5'
record_name_to_query = '_0cf6f28bf9558bd26bb44c62ca02cc17.rocketsfronttets2.rockets-yj.com'
record_type_to_query = 'CNAME'

# 함수 호출로 레코드 값 조회
get_route53_record_value(zone_id_to_query, record_name_to_query, record_type_to_query)
print(get_route53_record_value)


# def delete_route53_record(zone_id, record_name, record_type):
#     # AWS 자격 증명 및 Route 53 클라이언트 생성
#     aws_access_key = aws_access_key_id
#     aws_secret_key = aws_secret_access_key
#     client = boto3.client('route53', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

#     # 레코드를 삭제할 호스트 존 ID, 레코드 이름 및 레코드 타입
#     hosted_zone_id = zone_id
#     record_set_name = record_name
#     record_set_type = record_type

#     try:
#         # Route 53 레코드 삭제 요청
#         response = client.change_resource_record_sets(
#             HostedZoneId=hosted_zone_id,
#             ChangeBatch={
#                 'Changes': [
#                     {
#                         'Action': 'DELETE',
#                         'ResourceRecordSet': {
#                             'Name': record_set_name,
#                             'Type': record_set_type,
#                             'TTL': 300,  # 수정: TTL 값 설정 (원하는 값으로 변경)
#                             'ResourceRecords': []  # 수정: 레코드 값 (빈 리스트로 설정)
#                         }
#                     }
#                 ]
#             }
#         )

#         # 삭제 요청에 대한 응답 확인
#         if response['ResponseMetadata']['HTTPStatusCode'] == 200:
#             print(f"Route 53 record '{record_set_name}' of type '{record_set_type}' deleted successfully.")
#         else:
#             print(f"Failed to delete Route 53 record. Response: {response}")

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


# # 레코드를 삭제할 호스트 존 ID, 레코드 이름 및 레코드 타입 지정
# zone_id_to_delete = 'Z0958311YBP9BJL383S5'
# record_name_to_delete = '_0cf6f28bf9558bd26bb44c62ca02cc17.rocketsfronttets2.rockets-yj.com'
# record_type_to_delete = 'CNAME'

# # 함수 호출로 레코드 삭제
# delete_route53_record(zone_id_to_delete, record_name_to_delete, record_type_to_delete)
