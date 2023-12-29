from django.contrib import admin

from .models import Product, productImage, cart

admin.site.register(Product)
admin.site.register(productImage)
admin.site.register(cart)
