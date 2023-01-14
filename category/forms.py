from django import forms
from resources.models import Category
#DataFlair
class CategoryCreate(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('User',)