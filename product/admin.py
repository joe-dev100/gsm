from django.contrib import admin

# Register your models here.

from .models import Product, ProductCodeBarre
admin.site.register(Product)
admin.site.register(ProductCodeBarre)