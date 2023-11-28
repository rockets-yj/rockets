import boto3

# AWS 자격 증묭을 설정합니다. 나중에 우리 웹을 도커나 쿠버네티스로 올리면 환경벼수로 가져와야 할 듯?
session = boto3.Session (
    
    aws_access_key_id = '',
    aws_secret_access_key= '',
    region_name= ''
)




def delete_domain():
    

    # Route 53 클라이언트를 생성합니다.
    client = session.client('route53')

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

    # 로드밸런서의 주소
    load_balancer_dns = "a5717e5247b5547faba07421ed3ac069-2028637785.ap-northeast-2.elb.amazonaws.com"


    response = client.change_resource_record_sets(
        HostedZoneId = hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': 'www.mario.rockets-yj.com', # 원하는 도메인 이름
                        'Type': 'CNAME', # ipv4 주소는 A, dns 는 CNAME ,
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': load_balancer_dns
                            },
                        ],
                    }
                },
            ]
        }
    )
    
if __name__ == '__main__':
    delete_domain()



    
#print(hosted_zone)
#print(hosted_zone_id)



