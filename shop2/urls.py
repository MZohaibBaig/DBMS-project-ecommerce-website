# shop2/urls.py
from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView # Add ProductDetailView

app_name = 'shop2'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    # NEW: URL for the detail page
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]