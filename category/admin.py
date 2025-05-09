from django.contrib import admin

# Register your models here.

from .models import Categorie
admin.site.register(Categorie)  # Register the Category model with the admin site.
