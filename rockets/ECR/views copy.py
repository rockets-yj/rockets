from django.http import JsonResponse
from django.shortcuts import render, redirect
import boto3
from ecr_functions import *
from rocket_admin.models import *

def create_ecr_view(request):
    # 유저정보 
    # Userinfo.objects.all()
    # 서비스 정보
    # Serviceaws.objects.all()

    return render(request,'ECR/create_ecr.html')
    try:
        result = ecr_create_test.create_ecr('test2')
        return JsonResponse({'message': result})
    except Exception as e:
        return JsonResponse({'message': result}, status=500)
    
def search_ecr_view(request):
    return render(request,'ECR/search_ecr.html')
   

def delete_repository(request):
    if request.method == 'POST' and request.is_ajax():
        repo_uri = request.POST.get('repo_uri')
        # 여기에서 repo_uri에 해당하는 ECR 삭제 로직을 추가하면 됩니다.
        # 삭제가 성공하면 JsonResponse({'message': 'success'}) 반환
        # 삭제가 실패하면 JsonResponse({'message': 'error'}) 반환
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'error'})

def search_result(request):
    query = request.GET.get('query', '')
    print(query)

    try:
        repositories = ecr_list_test.list_ecr()
        return render(request, 'ECR/search_result.html', {'repositories': repositories, 'query': query})
    except Exception as e:
        return render(request, 'ECR/search_result.html', {'error_message': str(e), 'query': query})
    return render(request, 'ECR/search_result.html')
    
