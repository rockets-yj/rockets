import boto3

def search_ecr_by_region(service_name, region):
    query = service_name
    ecr_client = boto3.client('ecr', region_name=region)

    try:
        response = ecr_client.describe_repositories()
        repositories = response['repositories']

        # 검색어에 부합하는 리포지토리 찾기
        matched_repositories = [repo for repo in repositories if query.lower() in repo['repositoryUri'].lower()]

        # 검색된 리포지토리 정보 출력
        for repo in matched_repositories:
            registry_id = repo['registryId']
            repository_name = repo['repositoryName']
            repository_uri_parts = repo['repositoryUri'].split('/')
            domain = '/'.join(repository_uri_parts[:-1])  # 마지막 부분을 제외한 나머지를 합침

            print(f"Registry ID: {registry_id}")
            print(f"Repository Name: {repository_name}")
            print(f"Repository URI: {domain}")
            print('-' * 40)

    except Exception as e:
        print(f'검색 실패 : {e}')

if __name__ == '__main__':
    search_ecr_by_region('mario', 'ap-northeast-2')  # 'your_region'을 실제 AWS 리전으로 대체해주세요
