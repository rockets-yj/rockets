from django.contrib import admin
from django.urls import path, include
from . import views
from login.views import cklogout

urlpatterns = [
    # path('status/pages', views.userStatusPage, name='mypage'),
    path('status/', views.viewServiceList, name='userStatusPage'),
    path('status/serviceInfo/', views.viewServiceInfo, name='serviceInfo'),
    path('status/serviceInfo/sts', views.viewServiceInfoStatus, name='serviceInfoStatus'),
    path('logoutadmin/', cklogout, name="logoutadmin"),
    path('serviceDelete/',views.serviceDelete , name='serviceDelete')
]