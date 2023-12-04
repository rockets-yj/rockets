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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rocketadmin/', include('rocket_admin.urls')),
    path('', include('myapp.urls')),
    path('login/', include('login.urls')),
    path('', include('signup.urls')),
    path('mypage/', include('hosting.urls')),
    path('mypage/', include('userStatus.urls')),
    path('ecr/',include('ECR.urls')),
    path('rocketadmin/', include('ECR.urls')),
    path('cloudfront/',include('hosting.urls')),  #cloudfrontTest 추후 삭제 예정
]
