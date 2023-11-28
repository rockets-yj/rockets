from django.contrib import admin
from django.urls import path, include
from . import views
from . import adminService
from login.views import cklogout


urlpatterns = [
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('user_list/', views.user_list, name="user_list"),
    path('service/', adminService.adminService, name='adminService'),  # 전체 서비스 목록 조회
    path('service/info/', adminService.adminServiceInfo, name='adminServiceInfo'),  # 전체 서비스 중 하나 상세 조회
    path('logoutadmin/', cklogout, name="logoutadmin"),
]