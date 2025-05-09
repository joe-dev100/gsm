from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, post_migrate
from django.dispatch import receiver

from vente.models import Facture, LigneFacture


@receiver(post_save, sender=LigneFacture)
def update_product_stock(sender, instance, created, **kwargs):
    
    if created:
        qty = instance.qty
        product = instance.product
        product.qtyStock -= qty
        product.save()
        # facture=instance.facture
        # facture.total += instance.total
        # facture.netPaye = facture.total - facture.remise
        # facture.save() 
        
         
   
        
# @receiver(post_save, sender=Facture)
# def update_vente(sender, instance, created, **kwargs):
#     vente=instance.vente
#     total=vente.total
#     net=instance.netPaye
#     print("****************** TOTAL VENTE **************************************")
#     print(total)
#     print("******************NET A PAYER **************************************")
#     print(net)
#     vente.total=0
#     vente.save()
#     print("******************TOTAL VENTE AVANT **************************************")
#     print(vente.total)
#     vente.total = net + total
#     print("******************TOTAL VENTE APRES **************************************")
#     print(vente.total)
#     vente.save()
      
        
