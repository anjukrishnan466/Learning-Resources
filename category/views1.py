from django.shortcuts import render , redirect
from resources.models import Category
from django.views import View
from resources.models import Category
from .forms import CategoryCreate
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
# Create your views here.

class CategoryView(View):
    
    form_class = CategoryCreate
    model=Category
    template_name="category/category_form.html"
    def get(self,request):
        form=self.form_class()
        context={'form':form}
        return render(request,self.template_name, context)  
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/category/index')            

        context={'form':form}
        return render(request,self.template_name, context)
    
class CategoryListView(ListView):

    model = Category
    template_name = "category/category_index.html"
    context_object_name = 'category'
    
class CategoryDeleteView(DeleteView):
    model = Category
    success_url ="/category/index"
    template_name = "category/category_confirm_delete.html"
    
   class FilmCreateView(FilmBaseView, CreateView): 