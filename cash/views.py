from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import  Sum,Count,Q
from cash.models import Cash, EntreeCash, SortieCash
from category.models import Categorie
from product.models import Product
from settings.models import Setting
from vente.models import Facture
from django.contrib import messages
from utils import numFacture
# Create your views here.

def cash_confirmation(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    total=Facture.objects.filter(utilisateur__login=request.user).aggregate(total=Sum('netPaye'))['total']
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
    cash.estConfirme=True
    user=request.user
    numFacture(user)
    cash.save()
    
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
        'cash':cash,
        'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
        'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
    }
    return redirect('dashboard:teller_page')

def entree_cash(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
   
    if request.method == 'POST':
        dollar = request.POST.get('dollar')
        franc = request.POST.get('franc')
        description = request.POST.get('description')
        if not dollar:
            dollar = 0
        if not franc:
            franc = 0
        if  description:
            entree = EntreeCash(
                date=datetime.now().date(),
                dollar=dollar,
                franc=franc,
                description=description,
                cash=cash,
            )
            entree.save()
    
        context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        }
        html = render(request, "cash/partial/response.html", context)
        return HttpResponse(html)
    
def sortie_cash(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
    if request.method == 'POST':
        dollar = request.POST.get('dollar')
        franc = request.POST.get('franc')
        description = request.POST.get('description')
        if not dollar:
            dollar = 0
        if not franc:
            franc = 0
        if  int(dollar) > cash.dollar or int(franc) > cash.franc:
            messages.error(request, "Le montant de la sortie ne peut pas être supérieur au montant du cash")
            context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            }
            html = render(request, "cash/partial/response.html", context)
            return HttpResponse(html)
        else:
            sortie = SortieCash(
                date=datetime.now().date(),
                dollar=dollar,
                franc=franc,
                description=description,
                cash=cash,
            )
            sortie.save()
    
        context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        }
        html = render(request, "cash/partial/response.html", context)
        return HttpResponse(html)
    
def delete_entree(request, pk):
    entree = EntreeCash.objects.get(id=pk)
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
    cash.dollar -= int(entree.dollar)
    cash.franc -= int(entree.franc)
    cash.save()
    entree.delete()
    context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        }
    html = render(request, "cash/partial/response.html", context)
    return HttpResponse(html)

def delete_sortie(request, pk):
    entree =SortieCash.objects.get(id=pk)
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.last()
    cash.dollar += int(entree.dollar)
    cash.franc += int(entree.franc)
    cash.save()
    entree.delete()
    context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        }
    html = render(request, "cash/partial/response.html", context)
    return HttpResponse(html)


def change_devise(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.last()
    s=Setting.objects.last()
    taux=s.taux
    if request.method == 'POST':
        dollar = request.POST.get('devise')
        if not dollar or int(dollar) == 0:
            messages.error(request, "Le montant de la devise ne peut pas être nul ou égal à zéro")
            context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            }
            html = render(request, "cash/partial/response.html", context)
            return HttpResponse(html)
        if int(dollar) > cash.dollar:
            messages.error(request, "Il y a pas assez de devise dans le cash")
            context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            }
            html = render(request, "cash/partial/response.html", context)
            return HttpResponse(html)
        montant_change = int(dollar) * taux
        cash.dollar += int(dollar)
        cash.franc -= int(montant_change)
        cash.save()
    
        context={
            'categories':categories,
            'articles':articles,
            'cash':Cash.objects.last(),
            'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
            'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
            'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
            'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
            'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        }
        msg=f"Le montant de {dollar} a été changé avec succès"
        messages.success(request, msg)
        html = render(request, "cash/partial/response.html", context)
        return HttpResponse(html)
    html = render(request, "cash/partial/response.html", context)
    return HttpResponse(html)