# shop2/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView  # Add DetailView
from .models import Products
from .forms import ProductForm

# View for adding a product
class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'shop2/product_form.html'  # Corrected path
    success_url = reverse_lazy('shop2:product-list')

# View for listing all products
class ProductListView(ListView):
    model = Products
    template_name = 'shop2/product_list.html'  # Corrected path
    context_object_name = 'products'
    ordering = ['-created_at']

# NEW: View for a single product's details
class ProductDetailView(DetailView):
    model = Products
    template_name = 'shop2/product_detail.html' # Corrected path
    context_object_name = 'product'