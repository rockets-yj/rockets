#from django.shortcuts import render,redirect
import boto3
import time
#from rocket_admin.models import Serviceaws, Userinfo


def request_certificate(service_name):

    acm_client = boto3.client('acm', region_name='us-east-1') 
    MAIN_DOMAIN = ".rockets-yj.com"
    #domain_name = str(request.POST.get("service_name"))+MAIN_DOMAIN # testservice.rockets-yj.com
    domain_name = str(service_name)+MAIN_DOMAIN 

    response = acm_client.request_certificate(
        DomainName=domain_name,
         ValidationMethod='DNS',  
        SubjectAlternativeNames=[
            f"*.{domain_name}", 
            ],
            )

    certificate_arn = response['CertificateArn']
    print(f"Certificate ARN: {certificate_arn}")


    return certificate_arn

def create_dns_record(arn):                             # route53 레코드 생성 
    # ACM 인증서 정보 가져오기
    acm_certificate_arn = arn
    time.sleep(5)
    acm_client = boto3.client('acm', region_name='us-east-1')  
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

        hosted_zone_id = "Z0958311YBP9BJL383S5"  
        response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )

        # 생성된 CNAME 레코드 확인
        change_info = response['ChangeInfo']
        status = change_info['Status']

        while status == 'PENDING':
            time.sleep(20)
            response = route53_client.get_change(Id=change_info['Id'])
            change_info = response['ChangeInfo']
            status = change_info['Status']

        if status == 'INSYNC':
            print(f"CNAME record created successfully for {record_name}")


def check_acm_certificate_status(arn):

    certificate_arn = arn
    acm_client = boto3.client('acm')

    try:
        response = acm_client.describe_certificate(
            CertificateArn=certificate_arn
        )

        # 발급 상태 확인
        certificate_status = response['Certificate']['Status']
        print(f"Certificate Status: {certificate_status}")
        # print(response['Certificate'])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    service_name = "iloveeunji"
    arn  = request_certificate(service_name)
    create_dns_record(arn)
    time.sleep(10)
    check_acm_certificate_status(arn)