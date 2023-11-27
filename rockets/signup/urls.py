from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.userSignup, name="userSignup"),
    path('userSign/',views.userSign, name="userSign")
]


