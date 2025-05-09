from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UniteVente(models.Model):
    CHOICES = (
        ('Activée','Activée'),('Désactivée','Désactivée')
    )
    unit = models.CharField(max_length=250, unique=True, verbose_name="Unité")
    unitTag = models.CharField(max_length=3, unique=True)
    created = models.DateField(auto_now_add=True, verbose_name="Date de creation")
    status = models.CharField(default="Activée", verbose_name="Status", choices=CHOICES, max_length=10)
    def __str__(self):
        return self.unitTag

    class Meta:
        db_table = 't_UniteVente'
        managed = True
        verbose_name = 'UniteVente'
        verbose_name_plural = 'UniteVentes'


