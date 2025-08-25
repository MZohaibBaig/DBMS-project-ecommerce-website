from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "shop2/product_list.html"  # adjust if yours is different
    context_object_name = "products"
    paginate_by = 20

    # Make sure ordering uses the Python attribute names (not DB column names)
    def get_queryset(self):
        qs = super().get_queryset()
        # order by Python field name which maps to CreatedAt
        return qs.order_by("-created_at")


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop2/product_detail.html"  # adjust if yours is different
    context_object_name = "product"
    pk_url_kwarg = "pk"  # default; change if your URL uses another kwarg


class ProductCreateView(CreateView):
    model = Product
    template_name = "shop2/product_form.html"  # adjust if yours is different
    # Only include columns you actually want users to set (timestamps come from DB)
    fields = [
        "name",
        "description",
        "price",
        "stock_quantity",
        "image_url",
        "style",
        "material",
        "ar_model_url",
        "emb1",
        "emb2",
        "emb3",
        "emb4",
        "emb5",
    ]
    success_url = reverse_lazy("product-list")  # ensure your URL is named accordingly
