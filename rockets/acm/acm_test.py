from django.shortcuts import render,redirect
import boto3
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

if __name__ == "__main__":
    
    request_certificate("testservice")