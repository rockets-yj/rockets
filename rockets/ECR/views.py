from django.http import JsonResponse
import boto3
from ecr_functions import ecr_create_test

def create_ecr(request):

    try:
        result = ecr_create_test.create_ecr('test2')
        return JsonResponse({'message': result})
    except Exception as e:
        return JsonResponse({'message': result}, status=500)
