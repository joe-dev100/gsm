from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from category.models import Categorie
from django.contrib import messages
from django.db.models import  Sum,Count
from django.db.models import Q
from django.db.models import Count
from product.models import Product
from user.models import User
from vente.models import Facture
# Create your views here.
@login_required
def index(request):
    return render(request,'dashboard/index.html')

# @login_required
def teller_view(request):
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    total=Facture.objects.filter(utilisateur__login=request.user).aggregate(total=Sum('netPaye'))['total']
    articles= Product.objects.all().order_by('libelle')
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
    }
    
    return render(request,'teller/index.html',context)


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
