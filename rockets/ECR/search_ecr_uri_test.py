import boto3
from ecr_list_test import list_ecr  # 실제 모듈이 있는 경로로 수정

def search_ecr(service_name):
    query = service_name
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        response = ecr_client.describe_repositories()
        repositories = response['repositories']

        # 검색어에 부합하는 리포지토리 찾기
        matched_repositories = [repo for repo in repositories if query.lower() in repo['repositoryUri'].lower()]

        # 검색된 리포지토리 정보 출력
        for repo in matched_repositories:
            print(f"Registry ID: {repo['registryId']}")
            print(f"Repository Name: {repo['repositoryName']}")
            print(f"Repository URI: {repo['repositoryUri']}")
            print('-' * 40)

    except Exception as e:
        print(f'검색 실패 : {e}')

if __name__ == '__main__':
    search_ecr('pythontoecr')
