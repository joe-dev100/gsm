from typing import Iterable
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.db import models
from category.models import Categorie
from unity.models import UniteVente
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


class Product(models.Model):
    CHOICES = (
        ('EXP',"Oui le produit a une date d'expiration"),('NOTEXP',"Non le produit n'expire jamais")
    )
    STATUT = (
        ('Activé','Activé'),('Désactivé','Désactivé') ,('Expiré','Expiré'),('Supprimé','Supprimé')
    )
    codeRef = models.CharField(max_length=6, verbose_name="Code", validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,null=True,blank=True)
    unity = models.ForeignKey(UniteVente, on_delete=models.CASCADE,null=True,blank=True)
    libelle = models.CharField(max_length=255, verbose_name="Libellé article", unique=True)
    stockAlert = models.IntegerField(verbose_name="Stock alerte", default=5,null=True,blank=True)
    qtyStock =models.SmallIntegerField(verbose_name=_("Qté en stock"), default=0)
    description = models.CharField(max_length=255,verbose_name="Déscription", blank=True, null=True)
    qteEnVente = models.PositiveIntegerField(verbose_name="Qté en vente")
    price = models.PositiveIntegerField(verbose_name="Prix de vente",default=0)
    canExpiried = models.BooleanField(default=False, verbose_name="Produit avec date d'expiration ?")
    expiried_on = models.DateField(blank=True, null=True)
    barreCode = models.CharField(verbose_name="Barre Code", max_length=50,blank=True, null=True, validators=[MinLengthValidator(10), MaxLengthValidator(16)])
    status = models.CharField(default="Activé", verbose_name="Statut", choices=STATUT, max_length=10)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 't_Product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def save(self, *args, **kwargs):
        if self.expiried_on:
            self.canExpiried = True
        self.full_clean()
        return super(Product, self).save(*args, **kwargs)

class ProductCodeBarre(models.Model):
    codeBarre = models.CharField(max_length=30)
    status = models.BooleanField(default=True, verbose_name="Status")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.libelle

    class Meta:
        db_table = 't_ProductCodeBarre'
        managed = True
        verbose_name = 'ProductCodeBarre'
        verbose_name_plural = 'ProductCodeBarres'
        
        
        
class DateExpiration(models.Model):
    date=models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.libelle

    class Meta:
        db_table = 't_DateExpiration'
        managed = True
        verbose_name = "Date d'expiration"
        verbose_name_plural = "Dates d'expiration"