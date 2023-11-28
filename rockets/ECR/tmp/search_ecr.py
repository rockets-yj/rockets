
import boto3
from . import ecr_list_test 

# def search_ecr(request):
#     query = request.GET.get('query', '')
#     ecr_client = boto3.client('ecr')  # AWS 리전 지정

#     try:
#         response = ecr_client.describe_repositories()
#         repositories = response['repositories']

#         # 검색어에 부합하는 리포지토리 찾기
#         matched_repositories = [repo for repo in repositories if query.lower() in repo['repositoryUri'].lower()]

#         return render(request, 'ECR/search_ecr.html', {'repositories': matched_repositories, 'query': query})
#     except Exception as e:
#         return render(request, 'ECR/search_ecr.html', {'error_message': str(e), 'query': query})



def search_ecr(servie_name):
    query = servie_name
    ecr_client = boto3.client('ecr')  # AWS 리전 지정

    try:
        response = ecr_client.describe_repositories()
        repositories = response['repositories']

        # 검색어에 부합하는 리포지토리 찾기
        matched_repositories = [repo for repo in repositories if query.lower() in repo['repositoryUri'].lower()]
        print(matched_repositories)

    except Exception as e:
        print(f'검색 실패 : {e}')

if __name__ == '__main__':
    #list_ecr()
    search_ecr('pythontoecr')