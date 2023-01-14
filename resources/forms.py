from django import forms
from .models import Resources
from .models import TimeSpendUser
from django.core.validators import MinValueValidator, MaxValueValidator
# DataFlair


class ResourcesCreate(forms.ModelForm):
    class Meta:
        model = Resources
        exclude = ('User',)

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )