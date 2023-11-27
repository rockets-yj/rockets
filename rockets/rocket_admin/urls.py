from django.contrib import admin
from django.urls import path, include
from . import views
from . import userlist


urlpatterns = [
    path('userlist', userlist.viewUserlist, name='userlist')
]
