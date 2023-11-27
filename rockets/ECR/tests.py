import os
import django
from django.test import RequestFactory
import sys

# 현재 스크립트의 디렉토리를 Django 프로젝트의 루트로 변경
script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(script_path, ".."))  # 프로젝트 디렉토리의 상위 디렉토리
sys.path.insert(0, '/home/rocket/web/rockets')

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecr_manager.settings")
django.setup()

# Django 애플리케이션 뷰 함수 호출
from ecr_app.views import create_ecr, ecr_list

# 가상의 HTTP POST 요청 생성
request = RequestFactory().post('/create/', {'name': 'MyECR', 'description': 'My ECR Repository'})

# 함수 호출
response = create_ecr(request)

# 결과 확인
print(response)

# ECR 리스트 출력 (ecr_list 함수 호출)
ecr_list_response = ecr_list(RequestFactory().get('/list/'))

# ECR 리스트 출력
print("ECR List:")
for ecr in ecr_list_response.context['ecrs']:
    print(f"{ecr.name} - {ecr.description}")
