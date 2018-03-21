# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import get_template

#首页，登录页，注册页面
from bookapp.forms import *


def welcome(request):
    #t = get_template('welcome.html')
    return HttpResponse(render(request, 'welcome.html'));

def index(request):
    '''首页视图'''
    template_var={"w":_("欢迎您 游客!")}
    if request.user.is_authenticated == True:
        template_var["w"]=_("欢迎您 %s!")%request.user.username

    return HttpResponse(render(request, 'success.html'));


'''注册视图'''
def register(request):
    template_var = {}
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            newpassword = form.cleaned_data["newpassword"]
            email = form.cleaned_data["email"]
            #if password != newpassword:
               # return HttpResponse('确认登录密码与登录密码不一致');
            user = User.objects.create(email=email, password=password,username=username)
            user.save()
            _login(request, username, password)  # 注册完毕 直接登陆
            return HttpResponseRedirect('/book/list/')
    template_var["form"] = form
    return HttpResponse(render(request,'registration/register.html',{'form':template_var["form"]}));



'''登录视图'''
def login(request):
    template_var = {}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            if(True == _login(request,form.cleaned_data["username"],form.cleaned_data["password"])):
                return HttpResponseRedirect('/book/list/')
    #t=get_template('registration/login.html')
    #c = RequestContext(request, locals())

    template_var["form"] = form
    return HttpResponse(render(request, 'registration/login.html', {'form': template_var["form"]}));


'''登录核心方法'''
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
    return HttpResponseRedirect('/book/list/')

'''编辑个人信息'''
def account_edit(request):
    try:
        account_instance = UserProfile.objects.get(id=request.user.id)
    except UserProfile.DoesNotExist:
        account_instance = None
    form = AccountForm(request.POST or None,instance=account_instance)
    if form.is_valid():
        form.save()
        form = AccountForm

    return HttpResponse(render(request, 'registration/account_edit.html',{'form': form}));



#================================================================================================
#书籍相关

'''创建书'''
def create_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookForm()
    return HttpResponse(render(request,'bookapp/create_book.html',{'form': form}))

'''图书列表'''
def list_book(request):
    list_items = Book.objects.all()
    paginator = Paginator(list_items,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    return HttpResponse(render(request, 'bookapp/list_book.html'))

'''查找图书'''
def search_book(request,query):
    search_items = Book.objects.filter(title_contains=query)
    paginator = Paginator(search_items,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        search_items = paginator.page(page)
    except:
        search_items = paginator.page(paginator.num_pages)
    return HttpResponse(render(request, 'bookapp/search_book.html'))

'''管理图书信息'''
def manage_book(request):
    list_items = Book.objects.all()
    paginator = Paginator(list_items,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)
    return HttpResponse(render(request, 'bookapp/manage_book.html'))

'''图书列表信息'''
def list_book(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            if(True == _login(request,form.cleaned_data["username"],form.cleaned_data["password"])):
                return HttpResponseRedirect('/book/list/')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST.copy())
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username,email,password)
            user.save()
            _login(request,username,password)  #注册完毕 直接登录
            return HttpResponseRedirect('/book/list/')

    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST.copy())
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_items = Book.objects.filter(title__contains=query)

            paginator = Paginator(search_items,10)
            try:
                page = int(request.GET.get('page','1'))
            except ValueError:
                page = 1
            try:
                search_items = paginator.page(page)
            except:
                search_items = paginator.page(paginator.num_pages)
            return HttpResponse(render(request, 'bookapp/search_book.html'))

    list_items = Book.objects.all()
    paginator = Paginator(list_items,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
    return HttpResponse(render(request, 'bookapp/list_book.html'))

'''查看图书信息'''
def view_book(request,id):
    item = Book.objects.get(id=id)
    return HttpResponse(render(request, 'bookapp/view_book.html'))

'''编辑图书信息'''
def edit_book(request,id):
    book_instance = Book.objects.get(id=id)
    form = BookForm(request.POST or None,instance= book_instance)
    if form.is_valid():
        form.save()
    return HttpResponse(render(request, 'bookapp/edit_book.html'))






