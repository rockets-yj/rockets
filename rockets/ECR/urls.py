"""
URL configuration for rockets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# ecr_app/urls.py
from . import views
#from .search_ecr import *
#from functions import search_ecr
from ecr_functions import *
from ECR.views import search_ecr_view, delete_repository



urlpatterns = [
    path('create_ecr/', views.create_ecr_view, name='create_ecr_view'),
    # path('list/', ecr_list, name='ecr_list'),
    # path('ecr/', include('ecr_app.urls')),
    path('search_ecr/', views.search_ecr_view, name='search_ecr_view'),
    path('search_result/',views.search_result ,name='search_result'),
    #path('search_result/', search_ecr_view, name='search_result'),
    path('delete_repository/', delete_repository, name='delete_repository'),
]

