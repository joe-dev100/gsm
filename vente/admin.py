from django.contrib import admin
from .models import Session, Vente, Depense, Facture, LigneFacture, NumFacture
# Register your models here.

admin.site.register([
    Session,
    Vente,
    Depense,
    Facture,
    LigneFacture,
    NumFacture
])
