

import boto3
from . import ecr_list_test

def search_ecr(query):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        response = ecr_client.describe_repositories()
        repositories = response['repositories']

        # 검색어에 부합하는 리포지토리 찾기
        matched_repositories = [repo for repo in repositories if query.lower() in repo['repositoryUri'].lower()]

        return matched_repositories
    except Exception as e:
        print(f'검색 실패 : {e}')
        return []

def search_ecr_view(request):
    query = request.GET.get('query', '')
    repositories = search_ecr_view(query)
    return render(request, 'ECR/search_result.html', {'filtered_repositories': repositories, 'query': query})


def delete_ecr_repository(repo_name):
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        # ECR 리포지토리 삭제
        delete_response = ecr_client.delete_repository(repositoryName=repo_name, force=True)
        print(f'삭제 성공 {delete_response}')
        return delete_response
    except ecr_client.exceptions.RepositoryNotFoundException:
        print(f'삭제할 리포지토리가 존재하지 않습니다.')
        return {'message': 'Repository does not exist.'}
    except Exception as e:
        print(f'삭제에 실패했습니다: {e}')
        return {'error_message': str(e)}

if __name__ == '__main__':
    #list_ecr()
    search_ecr('12060233')
