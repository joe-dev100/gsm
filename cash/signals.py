from django.db.models.signals import post_save
from django.dispatch import receiver

from cash.models import EntreeCash, SortieCash


@receiver(post_save, sender=EntreeCash)
def entree_cash(sender, instance, created, **kwargs):
    from .models import Cash
    cash = Cash.objects.last()
    cash.dollar += int(instance.dollar)
    cash.franc += int(instance.franc)
    cash.save()
        
        
@receiver(post_save, sender=SortieCash)
def sortie_cash(sender, instance, created, **kwargs):
    from .models import Cash
    cash = Cash.objects.last()
    cash.dollar -= int(instance.dollar)
    cash.franc -= int(instance.franc)
    cash.save()
    