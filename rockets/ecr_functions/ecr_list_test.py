import boto3

def list_ecr(query=''):
    try:
        # AWS 리전 지정
        ecr_client = boto3.client('ecr')

        # ECR에서 저장소 목록을 가져옵니다.
        response = ecr_client.describe_repositories()
        repositories = response.get('repositories', [])  # 'repositories' 키가 없으면 빈 리스트를 반환

        # 검색 쿼리에 따라 저장소를 필터링합니다.
        filtered_repositories = filter_repositories(repositories, query)

        print(f'ECR List: {response}')
        return filtered_repositories
    except Exception as e:
        print(f'다시 시도해주세요: {e}')
        return {'error_message': str(e)}

def filter_repositories(repositories, query):
    # 저장소의 이름을 기반으로 필터링하는 예시
    filtered_repositories = [repo for repo in repositories if query.lower() in repo.get('repository_name', '').lower()]
    return filtered_repositories






 # 스크립트로 직접 실행될 때 수행되는 코드 (콘솔에서 확인)
if __name__ == '__main__':
    result = list_ecr()

    # 여기서는 단순히 결과를 출력할 수도 있습니다.
    print(result)
