from django.contrib import admin
from django.urls import path, include
from . import views
from login.views import cklogout

urlpatterns = [
    # path('status/', views.userStatusPage, name='userStatusPage'),
    path('status/', views.viewServiceList, name='userStatusPage'),
    path('status/serviceInfo/', views.viewServiceInfo, name='serviceInfo'),
    path('logoutadmin/', cklogout, name="logoutadmin"),
]