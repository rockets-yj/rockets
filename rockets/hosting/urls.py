from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('hosting/', views.userhostingPage, name='userHostingPage'),
    path('hosting/activate/', views.all_in_one, name='hosting'),
]
