from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        print("로그인 OK")
        return True
    else :
        print("로그인 내역x")
        return False
    