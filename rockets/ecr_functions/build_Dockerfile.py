import subprocess
import shlex
import boto3

def create_ecr_and_push_image(service_name, region):
    # Step 1: Create ECR repository
    ecr_client = boto3.client('ecr', region_name=region)
    repository_name = service_name

    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        print(f"ECR Repository 생성 성공: {response}")
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f"ECR Repository가 이미 존재합니다: {repository_name}")
    except Exception as e:
        print(f"ECR Repository 생성 실패: {e}")
        return

    # Step 2: Build Docker image
    try:
        subprocess.run(['docker', 'build', '-t', f'{repository_name}-image', '.'])
    except Exception as e:
        print(f"Docker 이미지 빌드 실패: {e}")
        return

    # Step 3: Tag Docker image for ECR
    try:
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        ecr_repository_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:latest"
        subprocess.run(['docker', 'tag', f'{repository_name}-image:latest', ecr_repository_uri])
    except Exception as e:
        print(f"Docker 이미지를 ECR에 태깅하는 중 오류 발생: {e}")
        return

    # Step 4: Login to ECR
    try:
        login_cmd = subprocess.run(shlex.split(f'aws ecr get-login-password --region {region}'), capture_output=True, text=True)
        login_token = login_cmd.stdout.strip()  # 토큰에서 공백을 제거합니다.

        # 토큰을 파일에 저장합니다.
        with open('ecr_login_token.txt', 'w') as file:
            file.write(login_token)

        # 저장된 파일을 사용하여 Docker에 로그인합니다.
        subprocess.run(['docker', 'login', '--password-stdin', '--username', 'AWS', f'https://{account_id}.dkr.ecr.{region}.amazonaws.com'], input=login_token, text=True)
    except subprocess.CalledProcessError as e:
        print(f"ECR에 로그인 중 오류 발생: {e}")
        return

    # Step 5: Push Docker image to ECR
    try:
        subprocess.run(['docker', 'push', ecr_repository_uri])
        print("Docker 이미지를 ECR에 성공적으로 푸시했습니다.")
    except Exception as e:
        print(f"Docker 이미지를 ECR에 푸시하는 중 오류 발생: {e}")

if __name__ == '__main__':
    create_ecr_and_push_image('mario', 'ap-northeast-2')  # 'your_region'을 실제 AWS 리전으로 대체해주세요
