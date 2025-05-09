from django.db import models

class Setting(models.Model):
    compony_name=models.CharField(max_length=255,verbose_name="Nom de l'entréprise", blank=True,null=True)
    compony_slogan=models.CharField(max_length=255,verbose_name="Slogan de l'entréprise", blank=True,null=True)
    compony_rccm=models.CharField(max_length=255,verbose_name="N° RCCM de l'entréprise", blank=True,null=True)
    compony_idnat=models.CharField(max_length=255,verbose_name="ID Nat de l'entréprise", blank=True,null=True)
    compony_adress=models.CharField(max_length=255,verbose_name="Adresse de l'entréprise", blank=True,null=True)
    compony_country=models.CharField(max_length=255,verbose_name="Adresse de l'entréprise", blank=True,null=True)
    compony_city=models.CharField(max_length=255,verbose_name="Adresse de l'entréprise", blank=True,null=True)
    compony_phone=models.CharField(max_length=255,verbose_name="Téléphone de l'entréprise", blank=True,null=True)
    compony_email=models.CharField(max_length=255,verbose_name="Adresse mail de l'entréprise", blank=True,null=True)
    compony_province=models.CharField(max_length=255,verbose_name="Adresse de l'entréprise", blank=True,null=True)
    compony_adress=models.CharField(max_length=255,verbose_name="Adresse de l'entréprise", blank=True,null=True)
    taux=models.PositiveSmallIntegerField(default=2800, verbose_name="Taux de change", blank=True,null=True)
    remise=models.DecimalField(default=0, decimal_places=2, verbose_name='Remise sur vente', max_digits=15, blank=True,null=True)
    seuil_remise=models.BigIntegerField(default=0,verbose_name="Somme min. à beneficier de la remise ", blank=True,null=True)
    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self):
        return self.compony_name



