from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView

app_name = "shop2"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/add/", ProductCreateView.as_view(), name="product-add"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
