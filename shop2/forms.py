from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock_quantity", "image_url"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
