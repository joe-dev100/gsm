from django.db.models.signals import post_migrate
from django.dispatch import receiver


unities = [
        {"unit": "Millilitre", "unitTag": "Ml"},
        {"unit": "Centilitre", "unitTag": "Cl"},
        {"unit": "Litre", "unitTag": "L"},
        {"unit": "Milligramme", "unitTag": "Mg"},
        {"unit": "Grammes", "unitTag": "Gm"},
        {"unit": "Kilogrammes", "unitTag": "Kg"},
        {"unit": "Pièce", "unitTag": "Pc"},
        {"unit": "Boite", "unitTag": "Bte"},
        {"unit": "Paquet", "unitTag": "Pqt"},
        {"unit": "Sachet", "unitTag": "Sct"},
        {"unit": "Mètre", "unitTag": "M"},
        {"unit": "Centimètre", "unitTag": "Cm"},
        {"unit": "Millimètre", "unitTag": "Mm"},
        {"unit": "Dizaine", "unitTag": "Dz"},
        {"unit": "Douzaine", "unitTag": "Dzn"},
    ]

@receiver(post_migrate)
def create_categories(sender, **kwargs):
    from .models import UniteVente
    if sender.name == 'unity':
        if UniteVente.objects.count() < 1:
            # Créer les unités de vente par défaut
            # Remplacez 'unity' par le nom réel de votre application si nécessaire
            for u in unities:
                UniteVente.objects.get_or_create(unit=u["unit"], unitTag=u["unitTag"])