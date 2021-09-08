"""pur_beurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from search import views

urlpatterns = [
    url(r'^$', views.index),                               # "/" will call the method "index" in "search.views.py"
    url(r'^result/', views.result),
    url(r'^aliment/', views.aliment),
    url(r'^compte/', views.compte),
    url(r'^search/', include('search.urls')),
    url(r'^admin/', admin.site.urls),
]
