# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import get_template

#首页，登录页，注册页面
from bookapp.forms import *


def welcome(request):
    t = get_template('welcome.html')
    c = RequestContext(request,locals())

def index(request):
    '''首页视图'''
    template_var={"w":_("欢迎您 游客!")}
    if request.user.is_authenticated():
        template_var["w"]=_("欢迎您 %s!")%request.user.username
    t = get_template('bookapp/list_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


'''注册视图'''




def register(request):
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            newpassword = form.cleaned_data["newpassword"]
            email = form.cleaned_data["email"]
            if password != newpassword:
                return HttpResponse('重复登录密码与登录密码不一致');
            user = User.objects.create(email=email, password=password,username=username)
            user.save()
            return render(request,'success.html',{'username':username});
    return render(request,'registration/register.html',{'form':form});

'''登录视图'''
def login(request):
    template_var = {}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            if(True == _login(request,form.cleaned_data["username"],form.cleaned_data["password"])):
                return HttpResponseRedirect('/bookapp/book/list/')
    #t=get_template('registration/login.html')
    #c = RequestContext(request, locals())
    else:
        return render(request,'registration/login.html',{'error':'用户名或密码错误'})


'''登陆核心方法'''
def _login(request,username,password):
    ret = False
    user = authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            messages.add_message(request,messages.INFO,_('登录成功!'))
            ret = True
        else:
            messages.add_message(request,messages.INFO,_('登录失败!'))
    else:
        messages.add_message(request,messages.INFO,_('该用户不存在!'))
    return ret


'''注销视图'''
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/bookapp/book/list/')

def account_edit(request):
    try:
        account_instance = UserProfile.objects.get(id=request.user.id)
    except UserProfile.DoesNotExist:
        account_instance = None
    form = AccountForm(request.POST or None,instance=account_instance)
    if form.is_valid():
        form.save()
        form = AccountForm
    t = get_template('registration/account_edit.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



