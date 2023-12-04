import subprocess
import shlex
import boto3

def buildAndPush(service_name, region, repository_name):
    # 단계 1: Docker 이미지 빌드
    try:
        subprocess.run(['docker', 'build', '-t', f'{repository_name}-image', '.'])
    except Exception as e:
        print(f"Docker 이미지 빌드 실패: {e}")
        return

    # 단계 2: ECR용 Docker 이미지 태그
    try:
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        ecr_repository_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:latest"
        subprocess.run(['docker', 'tag', f'{repository_name}-image:latest', ecr_repository_uri])
    except Exception as e:
        print(f"Docker 이미지를 ECR에 태깅하는 중 오류 발생: {e}")
        return

    # 단계 3: ECR에 로그인
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

    # 단계 4: Docker 이미지를 ECR에 푸시
    try:
        subprocess.run(['docker', 'push', ecr_repository_uri])
        print("Docker 이미지를 ECR에 성공적으로 푸시했습니다.")
    except Exception as e:
        print(f"Docker 이미지를 ECR에 푸시하는 중 오류 발생: {e}")

if __name__ == '__main__':
    기존_ECR_리포지토리_이름 = 'test_ecr6848'  # 실제 ECR 리포지토리의 이름으로 대체해주세요
    buildAndPush('mario', 'ap-northeast-2', 기존_ECR_리포지토리_이름)
