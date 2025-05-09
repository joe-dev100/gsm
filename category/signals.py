from django.db.models.signals import post_migrate
from django.dispatch import receiver

 
categories = [
    {"name":'Télephone', "img":"categories/phone.png"},
    {"name":'Montre', "img":"categories/montre.png"},
    {"name":'Vélo', "img":"categories/velo.webp"},
    {"name":'Chaussure', "img":"categories/chaussure.png"},
    {"name":'Sac',"img":"categories/sac.png"},
    {"name":'Parfum', "img":"categories/parfum.webp"},
    {"name":'Toutes', "img":"categories/all.webp"},
    {"name":'Crème', "img":"categories/creme.jpg"},
    {"name":'Savon', "img":"categories/savon.jpg"},
    {"name":'Maquillage', "img":"categories/maquillage.avif"},
    {"name":'Montre connectée', "img":"categories/stock-img-03.png"},
    {"name":'Tablette',"img":"categories/tablette.avif"},
    {"name":'Accessoire', "img":"categories/accessoire.avif"},
    {"name":'Imprimante', "img":"categories/imprimante.webp"},
    {"name":'Air-pod', "img":"categories/airpod.png"},
    {"name":'Ampoules',"img":"categories/ampoule.avif"},
    {"name":'Casque audio',"img":"categories/casque.png"},
    {"name":'Téléviseur', "img":"categories/tv.png"},
    {"name":'Lotion', "img":"categories/lotion.webp"},
    {"name":'Savon liquide', "img":"categories/savonliquide.avif"},
    {"name":'Shampooing', "img":"categories/shanpoing.webp"},
    {"name":'Gel douche', "img":"categories/geldouche.webp"},
    {"name":'Dentifrice', "img":"categories/dentifrice.jpg"},
    {"name":'Brosse à dents',"img":"categories/brosse.webp"},
    {"name":'Rasoir', "img":"categories/rasoir.webp"},
    {"name":'Assiette', "img":"categories/assiette.webp"},
    {"name":'Verre', "img":"categories/tasse.jpg"},
    {"name":'Casserole', "img":"categories/casserole.avif"},
    {"name":'Couteau',"img":"categories/couteau2.jpg"},
    {"name":'Cuillère', "img":"categories/fourchette.jpg"},
    {"name":'Singlet', "img":"categories/singlet.jfif"},
    {"name":'T-shirt', "img":"categories/tshirt.jpg"},
    {"name":'Sous-vêtement', "img":"categories/sousvetement.jpg"},
    {"name":'Jouet', "img":"categories/jouet.jpg"},
    {"name":'Vivre-frais', "img":"categories/vivre.jpg"},
    {"name":'Coiffure', "img":"categories/coiffure.webp"},
    {"name":'Électroménager',"img":"categories/electromenager.jpg"},
]

@receiver(post_migrate)
def create_categories(sender, **kwargs):
    from .models import Categorie
    if sender.name == 'category':
        if Categorie.objects.count() < 1:# ← Remplace par le nom réel de ton app
            
            for c in categories:
                Categorie.objects.get_or_create(name=c["name"], img=c["img"])