from django import forms
from django.contrib.auth.models import User
#DataFlair
class UserCreate(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('User',)