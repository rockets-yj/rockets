from django.shortcuts import render,redirect
from rocket_admin.models import Userinfo
import datetime
from django.utils import timezone
from django.http import HttpResponse
from rocket_admin.models import Userinfo
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt 
def checkIDtest(request) :
    request.session['loginOk'] = False
    #print(request.session['loginOk'])
    if True:
    #if request.method == 'POST' or request.method == 'post' :
        #_LOGIN_ID = request.POST.get("LOGIN_ID")
        
        user_id = request.POST.get('user_id')

        _UID = 'test001'
        #_PASSWORD = request.POST.get("PASSWORD")
        _UPWD = '96b8c73aa9d2bc0c4020c2f26687c4c014d01534fb83a6460a1d8d71c9af106c'
        
        print(user_id)
        
        # 데이터베이스와 비교를 해서 uid 가 user_id 를 검색을 해서 있는지 없는지 확인
        # exists 를 사용해서 값이 있으면 True 없으면 False 를 반환해준다.
        if Userinfo.objects.filter(uid=user_id).exists() :
            
            print('존재하는 ID')
        
            getUserinfo = Userinfo.objects.get(uid=_UID)
            if getUserinfo.upwd == _UPWD :
                request.session["loginOk"] = True
                request.session["UNO"] = getUserinfo.uno
                request.session["UID"] = getUserinfo.uid; 
                # 로그인 하면 uid를 들고다니면서 계속 데이터베이스와 비교해서 사용할거임
                request.session["UPWD"] = getUserinfo.upwd
                request.session["UNAME"] = getUserinfo.uname
                request.session["EMAIL"] = getUserinfo.email
                #request.session["AUTH_ID"] = getUserinfo.AUTH_ID
                print(request.session["UID"])
                # del request.session["UID"] # 세션 삭제 
                if getUserinfo.uno == 1 :
                    return render(request,'hosting/hostingPage.html')
                else :
                    #return render(request,'mainmenu.html')
                    return render(request,'userStatus/userStatus.html')
            else :
                request.session['loginOk'] = False
                return render(request, 'login/login.html',{ 'error' : '비밀번호가 틀렸습니다' })
        else :
            print("아이디가 존재하지 않음")
        
        
        
        # if user is not None :
        #     print("로그인 확인")
        # elif user is None :
        #     print("로그인 실패")
    return render(request, "hosting/hostingPage.html")