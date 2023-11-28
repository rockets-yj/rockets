import boto3

def list_ecr():
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        response = ecr_client.describe_repositories()
        repositories = response['repositories']

        print(f'ECR List{response}')
        return repositories  # 반환값 변경
    except Exception as e:
        print(f'다시 시도해주세요 : {e}')
        return {'error_message': str(e)}  # 반환값 변경

 # 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ == '__main__':
    result = list_ecr()

    # 여기서는 단순히 결과를 출력할 수도 있습니다.
    print(result)
