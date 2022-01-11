"""LOGOS_POLYTECHNIKOS URL Configuration

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
from django.urls import path, include

from logos_app.views import (
    home_view,
    article_view,
    article_request,
    article_list_request,
    logout_user,
    login_user,
    magazine_list_request,
    magazine_view,
    article_new,
    author_article_list_request,
    articles_my

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('login/', login_user, name="login_user_url"),
    path('logout/', logout_user, name="logout_user_url"),
    path('magazine/<int:id>/load', article_list_request, name="article_list"),
    path('magazine/<int:id>/', magazine_view, name="magazine"),
    path('magazine/', magazine_list_request, name="magazine_list"),
    path('members/', include('django.contrib.auth.urls')),
    path('article/<int:id>/', article_view, name="article"),
    path('article/<int:id>/load', article_request, name="article_load"),
    path('newarticle/', article_new, name="article_new"),
    path('myarticles/', articles_my, name="articles_my"),
    path('myarticles/load', author_article_list_request, name="author_articles_load"),
]
