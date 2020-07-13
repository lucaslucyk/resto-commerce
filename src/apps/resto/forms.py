from django import forms
from apps.resto import models

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = '__all__'
        widgets = {
            'mp_access_token': forms.TextInput(attrs={'type': 'password'}),
        }
