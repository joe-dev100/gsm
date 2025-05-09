
from django.db import models
from product.models import Product
from time import  timezone
from datetime import datetime
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

class Entree(models.Model):
    libelle=models.CharField(max_length=255,verbose_name="Libellé d'entrée")
    dateEntree=models.DateField(auto_now_add=True)
    def __str__(self):
        return f'Entrée stock du {self.dateEntree}'

    def save(self, *args, **kwargs):
        self.dateEntree = datetime.now()
        super(Entree, self).save(*args, **kwargs)
    class Meta:
        db_table = 't_Entree'
        managed = True
        verbose_name = 'Entrée'
        verbose_name_plural = 'Entées'

class EntreeItems(models.Model):
    qty=models.IntegerField(default=0)
    entree=models.ForeignKey(Entree,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.entree.dateEntree}--{self.product}'

    class Meta:
        db_table = 't_DetailAppro'
        managed = True
        verbose_name = 'DetailAppro'
        verbose_name_plural = 'DetailAppros'
        
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)



# SORTIES STOCK
class SortieStock(models.Model):
    dateSortie=models.DateField(auto_now_add=True)
    libelle=models.CharField(max_length=255,verbose_name="Libellé de sortie")
    def __str__(self):
        return f'Sortie du {self.dateSortie}'

    def save(self, *args, **kwargs):
        self.dateSortie = datetime.now()
        super(SortieStock, self).save(*args, **kwargs)

    class Meta:
        db_table = 't_SortieStock'
        managed = True
        verbose_name = 'SortieStock'
        verbose_name_plural = 'SortieStocks'

class SortieItems(models.Model):
    qty=models.IntegerField(default=0)
    sortie=models.ForeignKey(SortieStock,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    motif = models.TextField(verbose_name="Motif de sortie")
    def __str__(self):
        return f'{self.sortie.dateSortie}--{self.product.libelle}'

    class Meta:
        db_table = 't_DetailSortie'
        managed = True
        verbose_name = 'DetailSortie'
        verbose_name_plural = 'DetailSorties'


@receiver(post_save, sender=EntreeItems)
def entree_stock_on_create(sender,created,instance,**kwargs):
    stocked_qty = instance.product.qtyStock
    appro_qty = instance.qty
    if created:
        value = stocked_qty  + appro_qty
        instance.product.qtyStock = 0
        instance.product.save()
        instance.product.qtyStock = value
        instance.product.save()
        
        
        
@receiver(post_save, sender=SortieItems)
def sortie_stock_on_create(sender,created,instance,**kwargs):
    stocked_qty = instance.product.qtyStock
    appro_qty = instance.qty
    if created:
        value = stocked_qty  - appro_qty
        instance.product.qtyStock = 0
        instance.product.save()
        instance.product.qtyStock = value
        instance.product.save()
        