from django.contrib import admin
from django.urls import path, include
from . import views
from . import adminService
from login.views import cklogout


urlpatterns = [
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('user_list/', views.user_list, name="user_list"),
    path('service/', adminService.adminService, name='adminService'),  # 서비스탭) 전체 서비스 목록 조회
    path('service/info/', adminService.adminServiceInfo, name='adminServiceInfo'), 
    path('user/service/', adminService.adminUserService, name='adminUserService'),   # 사용자탭) 사용자의 전체 서비스 조회
    path('user/service/info', adminService.adminUserServiceInfo, name='adminUserServiceInfo'),  # 사용자탭) 전체 서비스 중 하나 상세 조회
    # path('user/service/pages', adminService.adminUserServiceInfoPages, name='adminUserServiceInfoPages'),  # 사용자탭) 전체 서비스 중 하나 상세 조회
    path('logoutadmin/', cklogout, name="logoutadmin"),
]