"""focaloid_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from .import views
from .views import line_chart, line_chart_json

urlpatterns = [

    path('register', views.register, name="register"),
    path('login', views.login, name="account_login"),
    path('logout', views.logout, name="logout"),
    path('index', views.index, name="index"),
    path('store', views.store, name="store"),
    path('edit/<int:id>/', views.edit, name="accountedit"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('resourceIndex/<int:id>/', views.resourceIndex, name="resourceIndex"),
    path('home', views.home, name="home"),
    path('accountsResources/<int:id>/',
         views.accountsResources, name="accountsResources"),
    path('status_edit/<int:id>/', views.status_edit, name="status_edit"),
    path('search_accounts', views.search_accounts, name="search_accounts"),
    path('search_resourcelist', views.search_resourcelist,
         name="search_resourcelist"),
    path('assigned_resources/<int:id>/',
         views.assigned_resources, name="assigned_resources"),
    path('accountsResources_admin/<int:id>/<int:user_id>',
         views.accountsResources_admin, name="accountsResources_admin"),
    path('upload_user', views.upload_user, name="upload_user"),
    path('download_user', views.download_user, name="download_user"),
    path('chart', line_chart, name='accountline_chart'),
    path('chartJSON', line_chart_json, name='account_line_chart_json'),
    path('progress/<int:id>/',
         views.progress, name="progress"),
    path('user_pdf/<int:id>/', views.user_pdf, name="user_pdf"),
    path('user_progress/<int:id>/<int:user_id>',
         views.user_progress, name="user_progress"),












]
