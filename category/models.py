from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Categorie(models.Model):
    CHOICES = (
        ('Activée','Activée'),('Désactivée','Désactivée')
    )
    name = models.CharField(max_length=250,unique=True,verbose_name="Catégorie")
    status = models.CharField(default="Activée", verbose_name="Status", choices=CHOICES, max_length=10)
    img=models.ImageField(upload_to="categories/",verbose_name="Image",blank=True,null=True)
    created_at=models.DateField(auto_now_add=True,verbose_name="Date de creation")
    def __str__(self):
        return self.name

   