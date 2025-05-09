from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Personnel(models.Model):
    class STATUT(models.TextChoices):
        ENGAGE = "Engagé"
        DEMISSIONNE = "Démissionné"
        LICENCIE = "Licencié"
    class FONCTION (models.TextChoices):
        GERANT = "Gérant"
        CAISSIER = "Caissier"
        ADMIN = "Admin"
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nom = models.CharField(verbose_name="Nom", max_length=255)
    postnom = models.CharField(verbose_name="Post-nom", max_length=255)
    prenom = models.CharField(verbose_name="Prénom", max_length=255)
    fonction = models.CharField(verbose_name="Fonction", max_length=255,choices=FONCTION.choices, default=FONCTION.CAISSIER)
    salaire = models.IntegerField(verbose_name="Salaire")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    statut = models.CharField(verbose_name="Statut", max_length=100, choices=STATUT.choices, default=STATUT.ENGAGE)

    def __str__(self):
        return f'{self.nom}- {self.postnom}- {self.prenom}'


class Paie(models.Model):
    periode= models.DateField()
    personnel = models.ManyToManyField(Personnel, through='FichePaie', related_name='details_paie')
    estPaye= models.BooleanField(default=False)


    def __str__(self):
        return self.periode

    class Meta:
        db_table = 't_Paie'
        managed = True
        verbose_name = 'Paie'
        verbose_name_plural = 'Paies'
class Credit(models.Model):
    personnel=models.ForeignKey(Personnel, on_delete=models.CASCADE)
    paie=models.ForeignKey(Paie, on_delete=models.CASCADE)
    montant= models.IntegerField(default=0)
class FichePaie(models.Model):
    totalAbsences = models.IntegerField(default=0)
    penaliteAbsences = models.IntegerField(default=0)
    totalCredit = models.IntegerField(default=0)
    totalRetenu = models.IntegerField(default=0)
    netApayer = models.IntegerField(default=0)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    paie = models.ForeignKey(Paie, on_delete=models.CASCADE)

    def __str__(self):
        return self.personnel.nom

    class Meta:
        db_table = 't_Fiche_paie'
        managed = True
        verbose_name = 'Fiche_paie'
        verbose_name_plural = 'Fiche_paies'


class Absence(models.Model):
    fichePaie= models.ForeignKey(FichePaie, on_delete=models.CASCADE)
    nombre = models.IntegerField(default=0)
    def __str__(self):
        return self.fichePaie.personnel.nom

    class Meta:
        db_table = 't_Absence'
        managed = True
        verbose_name = 'Absence'
        verbose_name_plural = 'Absences'