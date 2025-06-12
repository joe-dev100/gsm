import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cash.models import Cash, EntreeCash, SortieCash
from category.models import Categorie
from django.contrib import messages
from django.db.models import  Sum,Count,Q

from product.models import Product
from user.models import User
from vente.models import Facture
# Create your views here.
@login_required
def index(request):
    return render(request,'dashboard/index.html')

@login_required
def teller_view(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    total=Facture.objects.filter(utilisateur__login=request.user, vente__dateVente=datetime.datetime.now().date()).aggregate(total=Sum('netPaye'))['total']
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
        'cash':cash,
        'date':datetime.datetime.now().date(),
        'entrees':EntreeCash.objects.filter(cash=cash).order_by('-date'),
        'sorties':SortieCash.objects.filter(cash=cash).order_by('-date'),
        'total_sortie_dollar':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
        'total_sortie_franc':SortieCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
        'total_entree_dollar':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('dollar'))['total'],
        'total_entree_franc':EntreeCash.objects.filter(cash=cash).aggregate(total=Sum('franc'))['total'],
    }
    
    return render(request,'teller/index.html',context)


def dashboard_view(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    total=Facture.objects.filter(utilisateur__login=request.user).aggregate(total=Sum('netPaye'))['total']
    articles= Product.objects.all().order_by('libelle')
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
    }
    
    return render(request,'dashboard/dashboard.html',context)


def filter_by_category(request,pk):
    articles= Product.objects.filter(categorie_id=pk).order_by('libelle')
    context={
        'articles':articles,
    }
    
    return render(request,'teller/partials/product_list.html',context)

def filter_by_all_category(request):
    articles= Product.objects.all().order_by('libelle')
    context={
        'articles':articles,
    }
    
    return render(request,'teller/partials/product_list.html',context)

def search_view(request):
    if request.method=="POST":
        q=request.POST.get('q')
        articles= Product.objects.filter(Q(codeRef__icontains=q) | Q(libelle__icontains=q) |  Q(barreCode__startswith=q)).order_by('libelle')
        context={
            'articles':articles,
        }
        
        return render(request,'teller/partials/product_list.html',context)


#TODO:implementer la logique du cash
#TODO:implementer la logique de depenses 