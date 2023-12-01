from django.contrib import admin
from django.urls import path, include
# ecr_app/urls.py
from . import views
#from .search_ecr import *
#from functions import search_ecr
from ecr_functions import *
from .views import *


urlpatterns = [
    path('create_ecr/', views.create_ecr, name='create_ecr'),
    path('search_ecr/', views.search_ecr_view, name='search_ecr_view'),
    path('delete_ecr/', views.delete_repository, name='delete_ecr'),
    path('search_result/',views.search_result ,name='search_result'),
    path('delete_ecr/<str:repository_name>/', views.delete_ecr, name='delete_ecr'),

    
]
