from django.shortcuts import render, redirect
from resources.models import Category
from django.views import View
from resources.models import Category
from .forms import CategoryCreate

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class CategoryBaseView(View):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('category:all')


class CategoryListView(CategoryBaseView, ListView):
    """View to list all Category.
    Use the 'Category_list' variable in the template
    to access all Category objects"""


class CategoryDetailView(CategoryBaseView, DetailView):
    """View to list the details from one Category.
    Use the 'Category' variable in the template to access
    the specific Category here and in the Views below"""


class CategoryCreateView(CategoryBaseView, CreateView):
    """View to create a new Category"""


class CategoryUpdateView(CategoryBaseView, UpdateView):
    """View to update a Category"""
    template_name_suffix='_update_form'


class CategoryDeleteView(CategoryBaseView, DeleteView):
    """View to delete a Category"""
     