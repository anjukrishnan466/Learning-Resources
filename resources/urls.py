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
    path('index', views.index, name="index"),
    path('store', views.store, name="store"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('assign/<int:id>/', views.assign, name="assign"),
    path('resourcesView/<int:id>/', views.resourcesView, name="resourcesView"),
    path('download/<int:id>/', views.download, name="download"),
    path('search_products', views.search_products, name="search_products"),
    path('home', views.home, name="home"),

    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),

    path('upload_resources', views.upload_resources, name="upload_resources"),
    path('download_resources', views.download_resources, name="download_resources"),




]
