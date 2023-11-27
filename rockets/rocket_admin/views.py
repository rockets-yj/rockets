from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import Userinfo
from django.http import HttpResponse
from django.utils import timezone
from rockets import loginTF

def adminLogin(request) :
    #return render(request, "rocket-admin/adminUser.html")
    if loginTF.loginTF(request):
        print('adminlogin')
        return HttpResponse(user_list(request))
    else :
        return redirect('/')

#admin main 페이지
#login -> admin 계정 로그인시 adminUser.html로 이동

#user 정보 가져오기 
@csrf_exempt
def user_list(request):
    print('user_list')
    userList = {}
    userList["user_list"] = Userinfo.objects.all()
    print(userList)
    return render(request, 'rocket-admin/adminUser.html', userList)

    #admin 계정일 때 가져오기 UID == admin 근데 어차피 지금 uno=1일 경우 admin으로 접속되니까 test001 아이디 사용하면 확인 가능
    # if request.session['UNO'] == 1 :
    #     userList = {}
    #     userList["userList"] = Userinfo.objects.all()
    #     return render(request, 'rocket-admin/adminUser.html', userList)

    # else :
    #     pass
    #     # return redirect('/')
    #     #회원은 userstatus로 근데 이미 회원은 user status로 가잖아.. 

