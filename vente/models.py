from datetime import datetime

from django.db import models

# Create your models here.
from product.models import Product
from django.contrib.auth import get_user_model

user = get_user_model()


class Session(models.Model):
    EstOuvert = models.BooleanField(default=False)
    login = models.ForeignKey(user, on_delete=models.CASCADE)
    LastDateOpen = models.DateTimeField(blank=True, null=True)
    LastDateClose = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.login.username

    class Meta:
        db_table = 't_Session'
        managed = True
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'


class Vente(models.Model):
    dateVente = models.DateField()
    total= models.IntegerField(default=0)
    total_franc = models.IntegerField(default=0)
    total_dollar = models.IntegerField(default=0)
    def __str__(self):
        return f'vente du {self.dateVente}'

    class Meta:
        db_table = 't_Vente'
        managed = True
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'

class Depense(models.Model):
    motif= models.TextField(verbose_name="Motif de dépense")
    montant_franc = models.IntegerField()
    montant_dollar = models.IntegerField()
    vente= models.ForeignKey(Vente, on_delete=models.CASCADE)
    def __str__(self):
        return self.motif

    class Meta:
        db_table = 't_Depense'
        managed = True
        verbose_name = 'Depense'
        verbose_name_plural = 'Depenses'

class Facture(models.Model):
    utilisateur = models.ForeignKey(Session, on_delete=models.CASCADE)
    numFacture = models.CharField(verbose_name="N° Facture", max_length=15)
    dateFacture = models.DateTimeField(auto_now_add=True)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='LigneFacture', related_name='Product_fact_Items')
    total = models.IntegerField(default=0)
    remise = models.IntegerField(default=0)
    netPaye = models.IntegerField(default=0)


    def __str__(self):
        return self.numFacture

    def save(self, *args, **kwargs):
        self.dateFacture = datetime.now()
        super(Facture, self).save(*args, **kwargs)

    class Meta:
        db_table = 't_Facture'
        managed = True
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    prix = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.facture.numFacture}--{self.product.libelle}'

    class Meta:
        db_table = 't_LigneFacture'
        managed = True
        verbose_name = 'LigneFacture'
        verbose_name_plural = 'LigneFactures'


class NumFacture(models.Model):
    lastNum = models.SmallIntegerField(verbose_name="Dernier Numéro de Facture", default=0)
    date =models.DateField()
    def __str__(self):
        return f'{self.lastNum}'

    class Meta:
        db_table = 't_NumFacture'
        managed = True
        verbose_name = 'NumFacture'
        verbose_name_plural = 'NumFactures'
        
        
        
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    prix = models.IntegerField(default=0)
    total = models.IntegerField(default=0)


    class Meta:
        db_table = 't_Cart'
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'