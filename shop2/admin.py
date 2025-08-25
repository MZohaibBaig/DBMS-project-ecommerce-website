# admin.py

from django.contrib import admin
# Import the models you want to see in the admin panel
from .models import Users, Products, Orders, Carts, Cartitems, Homeservicebookings, Customframeorders

# The admin.site.register() function tells Django to show the model on the admin page.
admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Carts)
admin.site.register(Cartitems)
admin.site.register(Homeservicebookings)
admin.site.register(Customframeorders)