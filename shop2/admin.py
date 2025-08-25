from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",              # universal primary key alias
        "name",
        "price",
        "stock_quantity",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description", "style", "material")
    list_filter = ("style", "material")
    ordering = ("-created_at",)
