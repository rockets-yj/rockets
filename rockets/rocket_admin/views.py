from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rocket_admin.models import Userinfo
from django.utils import timezone
import hashlib

#admin main 페이지
#user 정보 가져오기 

# 우린 admin index 없으니까 지금은 필요 없을듯? 
# @csrf_exempt
# def admin_index(request) :
#     if request.session['AUTH_ID'] == 1 :
#         return render(request,'rocket-admin/adminUser.html')
#     else :
#         pass
#         # return redirect('/')

@csrf_exempt
def user_list(request):
    #admin 계정일 때 가져오기 UID == admin? 
    if request.session['UID'] == 'admin' :
        userList = {}
        userList["userList"] = Userinfo.objects.all()
        #테스트 페이지
        return render(request, 'rocket-admin/adminUsertest.html', userList)
    else :
        pass
        #회원은 userstatus로 
        #return redirect('/')
