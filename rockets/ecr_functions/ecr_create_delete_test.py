#생성 후 바로 삭제

from django.http import JsonResponse
import boto3

def create_ecr(service_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정
    repository_name = service_name  # 원하는 ECR 레포지토리 이름 지정

    try:
        # ECR 리포지토리 생성
        response = ecr_client.create_repository(repositoryName=repository_name)
        
        print(f'생성 성공 {response}')
        return response
    except Exception as e:
        print(f'생성에 실패했습니다: {e}')
        return e

def delete_ecr(repository_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        # ECR 리포지토리 삭제
        response = ecr_client.delete_repository(repositoryName=repository_name, force=True)
        
        print(f'삭제 성공 {response}')
        return response
    except Exception as e:
        print(f'삭제에 실패했습니다: {e}')
        return e

# 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ =='__main__':
    repo_name = 'pythontoecr'

    # ECR 리포지토리 생성
    create_response = create_ecr(repo_name)

    # ECR 리포지토리 삭제
    delete_response = delete_ecr(repo_name)

