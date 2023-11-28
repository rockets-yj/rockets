from django.contrib import admin
from django.urls import path, include
from . import views
from . import adminService
from login.views import cklogout


urlpatterns = [
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('user_list/', views.user_list, name="user_list"),
    path('adminService/', adminService.adminService, name='adminService'), 
    path('logoutadmin/', cklogout, name="logoutadmin"),
]
