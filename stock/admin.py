from django.contrib import admin

# Register your models here.
from .models import Entree, EntreeItems, SortieStock, SortieItems

admin.site.register(Entree)
admin.site.register(EntreeItems)
admin.site.register(SortieStock)
admin.site.register(SortieItems)
