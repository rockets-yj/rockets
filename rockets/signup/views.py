from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import Userinfo
from django.utils import timezone
import hashlib
#hashlib: password sha256 사용할 수 있음 

def userSignup(request) :
    return render(request, "login/signup.html")

@csrf_exempt
def userSign(request) :
    # 회원가입
    # post 타입으로 넘어온 데이터 받기, 입력받은 password는 sha암호화하여 추가하기
    _LOGIN_ID = request.POST.get("id")
    _PASSWORD = request.POST.get("password")
    _shaPASSWORD = hashlib.sha256(_PASSWORD.encode()).hexdigest()
    _NAME = request.POST.get("name")
    _EMAIL = request.POST.get("email")
    _REGIST_DATE = timezone.now()
    
    # 아이디, 이름, 이메일 중복여부 확인 
    if Userinfo.objects.filter(uid=_LOGIN_ID).exists():
        return render(request, 'login/signup.html', {'error' : '이미 사용중인 아이디 입니다.'} )
    
    elif Userinfo.objects.filter(uname=_NAME).exists() :
        return render(request, 'login/signup.html', {'error' : '이미 사용중인 이름 입니다.'} )
    
    elif Userinfo.objects.filter(email=_EMAIL).exists() :
        return render(request, 'login/signup.html', {'error' : '이미 사용중인 이메일 입니다.'} )
    
    # 중복된 정보가 없으면 회원가입 후 DB 추가, login.html 페이지로 이동
    else : 
        query = Userinfo.objects.create(uid=_LOGIN_ID, uname=_NAME, upwd=_shaPASSWORD, email=_EMAIL, regist_date=_REGIST_DATE)
        return render(request, 'login/login.html')