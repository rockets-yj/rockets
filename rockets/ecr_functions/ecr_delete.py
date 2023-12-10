
from django.http import JsonResponse
import boto3


def delete_ecr(repository_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        # ECR 리포지토리 삭제
        response = ecr_client.delete_repository(repositoryName=repository_name, force=True)
        
        print(f'삭제 성공 {response}')
        return response
    except Exception as e:
        print(f'삭제에 실패했습니다: {e}')
        return {'error_message': str(e)}

# 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ =='__main__':
    repo_name = 'test-ecr6848'


    # ECR 리포지토리 삭제
    delete_response = delete_ecr(repo_name)

