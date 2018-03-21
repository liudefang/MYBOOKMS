# -*- encoding: utf-8 -*-
# @Time    : 2018-03-19 21:06
# @Author  : mike.liu
# @File    : urls.py
from django.conf.urls import  url

from bookapp import views

app_name='book'
urlpatterns = [

    url(r'^create/$', views.create_book,name='create_book'),
    url(r'^list/$', views.list_book,name= 'list_book' ),
    url(r'^edit/(?P<id>[^/]+)/$', views.edit_book,name='edit_book'),
    url(r'^view/(?P<id>[^/]+)/$', views.view_book,name='view_book'),
    url(r'^manage/$', views.manage_book,name='manage_book'),
    url(r'^search/$', views.search_book,name='search_book'),
]