from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # ✅ import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ redirect root "/" → "/products/"
    path('', RedirectView.as_view(url='/products/')),

    # ✅ include your app URLs
    path('', include('shop2.urls')),
]
