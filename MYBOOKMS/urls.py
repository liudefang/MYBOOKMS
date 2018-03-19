"""MYBOOKMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import  url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.urls import include

from bookapp import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'bookms.views.home', name='home'),
    # url(r'^bookms/', include('bookms.foo.urls')),



    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.welcome),
    url(r'^welcome$', views.welcome),

    url(r'^accounts/index$', views.index,name="accounts_index"),
    url(r'^accounts/register$', views.register,name="register"),
    url(r'^accounts/login$', views.login,name="login"),
    url(r'^accounts/logout$', views.logout,name="logout"),
    url(r'^accounts/edit$', views.account_edit,name="edit"),




]



urlpatterns += staticfiles_urlpatterns()