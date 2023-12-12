import boto3
import os

# AWS 자격 증묭을 설정합니다. 나중에 우리 웹을 도커나 쿠버네티스로 올리면 환경벼수로 가져와야 할 듯?


MAIN_DOMAIN = 'rockets-yj.com'

session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY',''),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY',''),
    region_name= os.environ.get('ASWS_RECGION','')
)    



client = session.client('route53')


def get_HostedZoneId():
    # 도메인 id 확인
    # 모든 hosted Zone 을 가져옴
    response = client.list_hosted_zones_by_name() 
    hosted_zone_id = None

    for hosted_zone in response['HostedZones']:
        if hosted_zone['Name'] == MAIN_DOMAIN + '.' :
            hosted_zone_id = hosted_zone['Id']
            break
    # /hostedzone/Z0958311YBP9BJL383S5 이런식으로 반환을 하기 때문에 앞의 /hostedzone/ 을 삭제한다
    hosted_zone_id = hosted_zone_id.split("/hostedzone/")[1]
    return hosted_zone_id



def list_domain_name():
    # Route 53 클라이언트 생성    
    # 모든 hosted Zone 을 가져옴
    response = client.list_hosted_zones_by_name()
    
    print("도메인 목록")
    for domain in response['HostedZones']:
        print(f"- {domain['Name']}")



# 도메인 목록 가져옴
def list_records():
    
    Hosted_Zone_Id = get_HostedZoneId()
    
    try:
        # 도메인에 대한 레코드 목록 가져오기
        response = client.list_resource_record_sets(HostedZoneId=Hosted_Zone_Id, StartRecordName=MAIN_DOMAIN, StartRecordType='CNAME')

        # 가져온 레코드 목록 출력
        print(f"도메인 {MAIN_DOMAIN}의 레코드 목록:")
        for record_set in response['ResourceRecordSets']:
            print(f"- {record_set['Name']} - Type: {record_set['Type']} - Value: {record_set['ResourceRecords'][0]['Value']}")
            
    except Exception as e:
        print(f"도메인 레코드 목록을 가져오는 중 오류가 발생했습니다: {e}")
    



# 도메인 목록 가져옴
def get_list_records():
    
    Hosted_Zone_Id = get_HostedZoneId()
    try:
        # 도메인에 대한 레코드 목록 가져오기
        response = client.list_resource_record_sets(HostedZoneId=Hosted_Zone_Id, StartRecordName=MAIN_DOMAIN, StartRecordType='CNAME')
        print(response)
        return response 
    except Exception as e:
        return print(f"도메인 레코드 목록을 가져오는 중 오류가 발생했습니다: {e}")



# 도메인 이름 중복 체크
def check_duplicate_domain(service_name):
    Hosted_Zone_Id = get_HostedZoneId()
    domain_name = 'www.'+service_name+"."+MAIN_DOMAIN 
    try:
        # 도메인에 대한 레코드 목록 가져오기
        response = get_list_records()
        
        # www.mario.rockets-yj.com. 이렇게 이름뒤에 . 이 붙어서 나옴 그래서 그걸 없애는 코드
        
        for record_set in response['ResourceRecordSets']:
            # 맨 뒤의 . 제거
            record_name = record_set['Name'][:-1] if record_set['Name'].endswith('.') else record_set['Name']
            if record_name == domain_name:
                print(f'중복된 도메인 이름 {service_name} 사용중')
                break
    except Exception as e:
        print(f"도메인 레코드 목록을 가져오는 중 오류가 발생했습니다: {e}")

    pass


if __name__ == '__main__':
    
    list_domain_name()
    list_records()
    check_duplicate_domain('mario')