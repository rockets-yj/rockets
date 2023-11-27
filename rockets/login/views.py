from django.shortcuts import render,redirect
from rocket_admin.models import Userinfo
import datetime
from django.utils import timezone
from django.http import HttpResponse
from rocket_admin.models import Userinfo
from django.views.decorators.csrf import csrf_exempt
#import hashlib
#가영: 위에 import hashlib 사용하면 암호화된 암호 가져올 수 있습니다!(슬랙참고 후 주석삭제부탁드립니다!)

@csrf_exempt  
def cklogout(request) :
    request.session.clear() #모든 세션 삭제
    request.session['loginOk'] = False
    
    
    return redirect('/')

@csrf_exempt  
def ckMainmenu(request) :
    if request.session['loginOk'] is True :
        if request.session['AUTH_ID'] == 1 :
            return redirect('/adm/queenAdmin/')
        else :
            return render(request,'mainmenu.html')
    else :
        return redirect('/')
    

    
@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False