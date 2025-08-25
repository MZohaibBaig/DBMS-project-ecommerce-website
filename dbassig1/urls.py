# dbassig1/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop2.urls")),  # app_name in shop2/urls.py makes the "shop2:" namespace available
    # OR, equivalently:
    # path("", include(("shop2.urls", "shop2"), namespace="shop2")),
]