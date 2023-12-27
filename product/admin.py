from django.contrib import admin

from .models import Product, productImage

admin.site.register(Product)
admin.site.register(productImage)
