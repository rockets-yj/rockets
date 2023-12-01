from django.http import JsonResponse
from django.shortcuts import render, redirect
import boto3
from ecr_functions import *
from rocket_admin.models import *
from django.views.decorators.csrf import csrf_exempt
from ecr_functions import *
from ecr_functions.ecr_create_test import create_ecr_function
import json



def create_ecr(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        if service_name:
            service_name_lower = service_name.lower()  # 입력된 대문자를 소문자로 변환
            response = create_ecr_function(service_name_lower)
            return JsonResponse({'message': f'ECR repository created: {response}'})
        else:
            return JsonResponse({'error_message': 'Service name is required.'}, status=400)
    return render(request, 'ECR/create_ecr.html')




# ECR 삭제 함수
def delete_ecr(repository_name):
    ecr_client = boto3.client('ecr')
    
    print("delete_ecr :", repository_name)
    

    try:
        # ECR 리포지토리 삭제
        response = ecr_client.delete_repository(repositoryName=repository_name, force=True)
        print(f'삭제 성공 {response}')
        return response
    except Exception as e:
        print(f'삭제에 실패했습니다: {e}')
        return {'error_message': str(e)}

def create_ecr_view(request):
    return render(request, 'ECR/create_ecr.html')

@csrf_exempt
def delete_repository(request):
    if request.method == 'POST':
        repo_name = request.POST.get('repo_name')
        try:
            print(f'Deleting repository: {repo_name}')  # 추가한 부분            
            # 여기에서 repo_name에 해당하는 ECR 삭제 로직을 추가하면 됩니다.
            # 삭제가 성공하면 JsonResponse({'message': 'success'}) 반환
            # 삭제가 실패하면 JsonResponse({'message': 'error'}) 반환
            delete_response = delete_ecr(repo_name)
            return JsonResponse({'message': 'success'})
        except Exception as e:
            return JsonResponse({'message': 'error'}, status=500)
    else:
        return JsonResponse({'message': 'error'})

def search_ecr_view(request):
    return render(request, 'ECR/search_ecr.html')

def search_result(request):
    query = request.GET.get('query', '')

    try:
        # 검색 결과를 가져오는 함수 변경
        repositories = search_ecr.search_ecr(query)
        return render(request, 'ECR/search_result.html', {'filtered_repositories': repositories, 'query': query})
    except Exception as e:
        return render(request, 'ECR/search_result.html', {'error_message': str(e), 'query': query})