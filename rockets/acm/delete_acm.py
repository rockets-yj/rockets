import boto3

def search_acm(service_name):
    # AWS CLI의 configure와 같은 방식으로 AWS 자격 증명을 설정하거나,
    # 직접 Boto3 클라이언트를 생성하여 자격 증명을 전달할 수 있습니다.
    # 자세한 내용은 Boto3 문서를 참고하세요.
    acm_client = boto3.client('acm', region_name='us-east-1')  # 'your_region'을 사용하는 AWS 리전으로 변경

    MAIN_DOMAIN = ".rockets-yj.com"

    domain = service_name + MAIN_DOMAIN

    try:
        # ACM에서 인증서 목록 조회
        response = acm_client.list_certificates()

        # 특정 이름에 맞는 인증서의 ARN 찾기
        for certificate in response['CertificateSummaryList']:
            if certificate['DomainName'] == domain:
                return certificate['CertificateArn']

        # 특정 이름에 맞는 인증서가 없을 경우 None 반환
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    


def delete_acm(service_name):
    acm_client = boto3.client('acm', region_name='us-east-1')  # 'your_region'을 사용하는 AWS 리전으로 변경
    arn = search_acm(service_name)

    try:
        response = acm_client.delete_certificate(
            CertificateArn=arn
        )
        print(f"Certificate deletion initiated successfully for {arn}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
    

if __name__ == "__main__":
    service_name = "dockerzip12"
    delete_acm(service_name)