from django.contrib import admin
from .models import Cash, EntreeCash, SortieCash
# Register your models here.
admin.site.register([
    Cash,
    EntreeCash,
    SortieCash,
])
