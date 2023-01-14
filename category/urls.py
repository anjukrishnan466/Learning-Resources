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

from django.urls import path
from . import views
app_name = 'category'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='all'),
    path('category/<int:pk>/detail',
         views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(),
         name='category_create'),
    path('category/<int:pk>/update/',
         views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/',
         views.CategoryDeleteView.as_view(), name='category_delete'),

]
