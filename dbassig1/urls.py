from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    # one-time redirect from "/" to the product list
    path("", RedirectView.as_view(pattern_name="shop2:product-list", permanent=False)),

    # mount the app with a namespace so {% url 'shop2:...' %} works
    path("", include(("shop2.urls", "shop2"), namespace="shop2")),
]
