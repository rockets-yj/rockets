from django.http import JsonResponse
import boto3

def create_ecr(service_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정
    repository_name = service_name  # 원하는 ECR 레포지토리 이름 지정

    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        
        print(f'생성 성공 {response}')
        return response
        #return JsonResponse({'message': 'ECR repository created successfully.'})
    except Exception as e:
        print(f'생성에 실패했습니다 : {e}')
        return e
        #return JsonResponse({'message': str(e)}, status=500)


def create_ecr_function(service_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정
    repository_name = service_name.lower()  # 원하는 ECR 레포지토리 이름 지정 (소문자로 변환)

    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        print(f'생성 성공 {response}')
        return response
    except Exception as e:
        print(f'생성에 실패했습니다 : {e}')
        return {'error_message': str(e)}


 # 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ =='__main__':
    create_ecr('pythontoecr')

