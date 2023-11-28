from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import *

#views에서 유저 선택시 유저정보 가져오는 화면

def adminService(request):
    return render(request, "rocket-admin/adminService.html")
