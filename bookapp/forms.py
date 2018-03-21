#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2018/3/19 16:30
# @Author  : mike.liu
# @File    : forms.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from bookapp.models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['borrower', 'available', 'borrow_date',
                   'return_date']  # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)


class AccountForm(forms.ModelForm):
    email = forms.EmailField(label=_("邮件"), max_length=30, widget=forms.TextInput(attrs={'size': 30, }))
    username = forms.CharField(label=_("昵称"), max_length=30, widget=forms.TextInput(attrs={'size': 20, }))
    password = forms.CharField(label=_("密码"), max_length=30, widget=forms.PasswordInput(attrs={'size': 20, }))

    def clean_username(self):
        '''验证重复昵称'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("该昵称已经被使用请使用其他的昵称"))

    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_("该邮箱已经被使用请使用其他的"))

#注册信息的验证
class RegisterForm(forms.Form):
    email = forms.EmailField(label=_("邮件"),max_length=30,widget=forms.TextInput(attrs={'size':30,}))
    password = forms.CharField(label=_("密码"),max_length=30,widget=forms.PasswordInput(attrs={'size':20,}))
    newpassword = forms.CharField(label=_("确认密码"), max_length=30, widget=forms.PasswordInput(attrs={'size': 20, }))
    username = forms.CharField(label=_("昵称"),max_length=30,widget=forms.TextInput(attrs={'size':20,}))

    def clean_username(self):
        '''验证重复昵称'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("该昵称已经被使用请使用其他的昵称"))

    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_("该邮箱已经被使用请使用其他的"))

    def clean_passwd(self):
        '''验证密码和确认密码是否一致'''
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get("password")
        newpassword = cleaned_data.get("newpassword")
        if password and newpassword:
            if password != newpassword:
                msg = "确认登录密码与登录密码不一致!"
                self._errors["newpassword"] = self.error_class([msg])

        return cleaned_data



class LoginForm(forms.Form):
    username=forms.CharField(label=_("昵称"),max_length=30,widget=forms.TextInput(attrs={'size':20,}))
    password=forms.CharField(label=_("密码"),max_length=30,widget=forms.PasswordInput(attrs={'size':20,}))

    def clean_username(self):
        '''验证用户名是否正确'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if  users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("该用户不存在，请注册!"))

    def clean_password(self):
        '''验证密码是否正确'''
        password = User.objects.filter(password__iexact=self.cleaned_data["password"])
        if  password:
            return self.cleaned_data["password"]
        raise forms.ValidationError(_("密码错误!"))

class SearchForm(forms.Form):
    query=forms.CharField(label=_("查询"),max_length=30,widget=forms.TextInput(attrs={'size':20,}))
