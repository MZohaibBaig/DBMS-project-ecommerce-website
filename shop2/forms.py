# forms.py
from django import forms
from .models import Products # <-- FIXED

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products # <-- FIXED
        fields = ['name', 'description', 'price', 'stock_quantity', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }