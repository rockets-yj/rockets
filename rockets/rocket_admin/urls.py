from django.contrib import admin
from django.urls import path, include
from . import views
from . import userlist
from .views import user_list
from login.views import cklogout


urlpatterns = [
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('user_list/', views.user_list, name="user_list"),
    
    path('userlist', userlist.viewUserlist, name='userlist'), #이거 서비스리스트로 바꿔야할듯 
    path('logoutadmin/', cklogout, name="logoutadmin"),
]
