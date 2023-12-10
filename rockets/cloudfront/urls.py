from django.contrib import admin
from django.urls import path, include
from cloudfront import cf_create

urlpatterns = [
    path('testPage/', cf_create.getTestPage, name='testPage'),
    path('test/', cf_create.create_cloudfront_distribution, name='create_cloudfront'),
    path('createmain',cf_create.all_in_one , name='all_in_one')
]

