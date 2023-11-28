from django.http import JsonResponse
import boto3
import subprocess

def create_ecr(service_name):
    ecr_client = boto3.client('ecr')
    repository_name = service_name

    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        print(f'생성 성공 {response}')

        # Build Docker image
        subprocess.run(['docker', 'build', '-t', f'{repository_name}-image', '.'])

        # Tag Docker image for ECR
        subprocess.run(['docker', 'tag', f'{repository_name}-image:latest', f'<your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/{repository_name}:latest'])

        # Login to ECR
        subprocess.run(['aws', 'ecr', 'get-login-password', '--region', '<your-region>', '|', 'docker', 'login', '--username', 'AWS', '--password-stdin', f'<your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com'])

        # Push Docker image to ECR
        subprocess.run(['docker', 'push', f'<your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/{repository_name}:latest'])

        #return JsonResponse({'message': 'ECR repository and Docker image created and pushed successfully.'})
    except Exception as e:
        print(f'생성에 실패했습니다 : {e}')
        #return JsonResponse({'message': str(e)}, status=500)

# 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ == '__main__':
    create_ecr('mario')
