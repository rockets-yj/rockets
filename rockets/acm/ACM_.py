#from django.shortcuts import render,redirect
import boto3
import time
#from rocket_admin.models import Serviceaws, Userinfo

MAIN_DOMAIN = ".rockets-yj.com"

def request_certificate(service_name):
    acm_client = boto3.client('acm', region_name='us-east-1')  # 'your_region'을 사용하는 AWS 리전으로 변경
    #domain_name = str(request.POST.get("service_name"))+MAIN_DOMAIN # testservice.rockets-yj.com
    domain_name = str(service_name)+MAIN_DOMAIN # testservice.rockets-yj.com

    response = acm_client.request_certificate(
        DomainName=domain_name,
         ValidationMethod='DNS',  # DNS를 통한 도메인 확인을 선택할 수 있습니다.
        SubjectAlternativeNames=[
            f"*.{domain_name}",  # 와일드카드 인증서를 사용하려면 추가
            # 다른 대체 도메인을 필요에 따라 추가할 수 있습니다.
            ],
            )

    certificate_arn = response['CertificateArn']
    print(f"Certificate ARN: {certificate_arn}")

            # 인증서 발급 요청이 성공하면 DNS 확인을 수행해야 합니다.
            # ACM이 DNS 확인을 위한 레코드를 생성할 것이므로,
            # 인증서를 사용하는 도메인의 DNS 레코드가 ACM에서 관리되어야 합니다.

    return certificate_arn

def create_dns_record(service_name):
    # ACM 인증서 정보 가져오기
    acm_certificate_arn = request_certificate(service_name)
    time.sleep(5)
    acm_client = boto3.client('acm', region_name='us-east-1')  # 'your_region'을 사용하는 AWS 리전으로 변경
    acm_certificate = acm_client.describe_certificate(CertificateArn=acm_certificate_arn)

    # Route 53 클라이언트 생성
    route53_client = boto3.client('route53')  

    # DNS 레코드 생성을 위한 정보 추출
    domain_name = acm_certificate['Certificate']['DomainName']
    validation_options = acm_certificate['Certificate']['DomainValidationOptions']

    
    for validation_option in validation_options:
        record_name = validation_option['ResourceRecord']['Name']
        record_value = validation_option['ResourceRecord']['Value']

        # Route 53에 CNAME 레코드 생성
        change_batch = {
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'CNAME',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }

        # 'yj.com' 호스트 영역 ID로 변경
        hosted_zone_id = "Z0958311YBP9BJL383S5"  
        response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )

        # 생성된 CNAME 레코드 확인
        change_info = response['ChangeInfo']
        status = change_info['Status']

        while status == 'PENDING':
            time.sleep(10)
            response = route53_client.get_change(Id=change_info['Id'])
            change_info = response['ChangeInfo']
            status = change_info['Status']

        if status == 'INSYNC':
            print(f"CNAME record created successfully for {record_name}")


if __name__ == "__main__":
    service_name = "acmtest3"
    create_dns_record(service_name)