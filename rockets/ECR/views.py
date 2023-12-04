from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ecr_functions import *
from rocket_admin.models import *
from django.views.decorators.csrf import csrf_exempt
from ecr_functions import *
from ecr_functions.ecr_create_test import create_ecr_function
from ecr_functions.create_build_push import create_ecr_and_push_image
import json
import boto3
import os
import subprocess
import re
import shlex



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
    


def push_to_ecr(request):
    if request.method == 'GET':
        service_name = request.GET.get('service_name')
        region = request.GET.get('region')
        search_keyword = request.GET.get('search_keyword')

        if not service_name or not region or not search_keyword:
            return JsonResponse({'message': '서비스 이름, 리전, 검색어를 모두 입력하세요.'})

        try:
            # 여기서 search_keyword를 사용하여 원하는 동작을 수행
            # 예를 들어, create_ecr_and_push_image 함수에 추가 파라미터로 전달할 수 있습니다.
            create_ecr_and_push_image(service_name, region, search_keyword)

            message = f"{service_name} 서비스에 대한 ECR 이미지가 성공적으로 푸시되었습니다."
        except Exception as e:
            message = f"에러: {e}"

        return JsonResponse({'message': message})
    else:
        return JsonResponse({'message': '잘못된 요청 메서드'})
    



def create_ecr_and_push_image(service_name, region):
    # Step 1: Create ECR repository
    ecr_client = boto3.client('ecr', region_name=region)
    repository_name = re.sub(r'[^a-z0-9_]', '_', service_name.lower())

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
        dockerfile_path = '/home/rocket/git-workspace/kim_git/rockets/rockets/ecr_functions/Dockerfile'
        dockerfile_directory = '/home/rocket/git-workspace/kim_git/rockets/rockets/ecr_functions'
        subprocess.run(['docker', 'build', '-t', f'{repository_name}-image', '-f', dockerfile_path, '.'], cwd=dockerfile_directory)
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

def create_ecr_and_push(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        region = request.POST.get('region')

        try:
            create_ecr_and_push_image(service_name, region)
            return HttpResponse(f"ECR 생성 및 이미지 빌드 및 푸시 성공! (서비스명: {service_name}, 리전: {region})")
        except Exception as e:
            return HttpResponse(f"에러 발생: {e}")
    else:
        return render(request, 'ECR/create_ecr_and_push.html')