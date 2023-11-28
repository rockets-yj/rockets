from django.shortcuts import render,redirect
from rocket_admin.models import Userinfo
import datetime
from django.utils import timezone
from django.http import HttpResponse
from rocket_admin.models import Userinfo
from django.views.decorators.csrf import csrf_exempt
import hashlib
from rocket_admin import views


def userLogin(request) :
    return render(request, "login.html")


@csrf_exempt   
def checkID(request) :
    request.session['loginOk'] = False
    #print(request.session['loginOk'])
    if request.method == 'POST' or request.method == 'post' :
        _UID = request.POST.get("uid")
        _UPWD = request.POST.get("upwd")
        _shaUPWD = hashlib.sha256(_UPWD.encode()).hexdigest()
        # 데이터베이스와 비교를 해서 uid 가 user_id 를 검색을 해서 있는지 없는지 확인
        # exists 를 사용해서 값이 있으면 True 없으면 False 를 반환해준다.
        if Userinfo.objects.filter(uid=_UID).exists() :
            print('존재하는 ID')
        
            getUserinfo = Userinfo.objects.get(uid=_UID)
            if getUserinfo.upwd == _shaUPWD :
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
                if getUserinfo.uno == 1 : # 관리자로 들어감-> uno==1을 관리자로 설정함
                    return redirect('/rocketadmin/adminLogin/')
                    #return HttpResponse(views.adminLogin(request))
                    #return render(request,'rocket-admin/adminUser.html')
                else :
                    #return render(request,'mainmenu.html')
                    # return render(request,'userStatus/userStatus.html')
                    return redirect('/mypage/status/')
            else :
                request.session['loginOk'] = False
                return render(request, 'login/login.html',{ 'error' : '비밀번호를 다시 입력하세요.' })
        else :
            print("아이디가 존재하지 않음")
            return render(request, 'login/login.html',{ 'error' : '아이디를 다시 입력하세요.' })
        
        
        # if user is not None :
        #      print("로그인 확인")
        # elif user is None :
        #      print("로그인 실패")
    return render(request, "login/login.html")


# 로그인 후 모든세션삭제
@csrf_exempt  
def cklogout(request) :
    request.session.clear() #모든 세션 삭제
    request.session['loginOk'] = False
    print("모든세션삭제 체크아웃")

    return redirect('/')


# 로그인 검증: 로그인 이후 다시 login 페이지에서 로그인이 유지됐는지 확인
# 위에 cklogout 후 다시 loginTF 실행시 로그인 내역x로 나오는지 확인
@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        print("로그인 OK")
        return redirect('/')
    else :
        print("로그인 내역x")
        return redirect('/')
    

# @csrf_exempt  
# def ckMainmenu(request) :
#     if request.session['loginOk'] is True :
#         if request.session['AUTH_ID'] == 1 : 
#             return redirect('/adm/queenAdmin/')
#         else :
#             return render(request,'mainmenu.html')
#     else :
#         return redirect('/')