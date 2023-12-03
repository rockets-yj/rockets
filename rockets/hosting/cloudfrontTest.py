from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *
from s3_functions import cf_create

# todo: 나중에 삭제하기
def cloudfrontTestPage(request):
    return render(request, 'cloudfront_test/cloudfront_create.html')

def cloudfrontCreate():
    print("여기?")
    cf_create.create_cloudfront_distribution()
