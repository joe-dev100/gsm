from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from product.models import Product
from stock.form import EntreeForm, EntreeItemsForm, SortieForm, SortieItemsForm
from .models import Entree, EntreeItems, SortieItems, SortieStock
from django.db.models import Count
# Create your views here.

# ENTREE STOCK
def entree_view(request):
    items=Entree.objects.all().annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
    products=Product.objects.filter(status="Activé").order_by('libelle')
    form=EntreeForm()
    context = {
        'items': items,
        'page': 'entree',
        'products': products,
        
    }
    if request.htmx:
        return render(request, 'stock/entree/partial/response.html', context)
    return render(request, 'stock/entree/entree_list.html',context)

def add_entree(request):
    items=Entree.objects.all().annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
    products=Product.objects.filter(status="Activé").order_by('libelle')
    
    context = {
        'entrees': items,
        'products': products,
        'page': 'entree',
        
    }
    if request.method == "POST":
        libelle = request.POST.get('libelle') 
        qty= request.POST.getlist('qty') 
        product= request.POST.getlist('product') 
        entree=Entree.objects.create(libelle=libelle)
        entree.save()
        for i in range(len(product)):
            if product[i] == '':
                Entree.objects.last().delete()
                messages.error(request, "Veuillez sélectionner un produit valide.")
                html = render(request, "stock/entree/partial/add_response.html", context)
                return HttpResponse(html)
            else:
                items=EntreeItems.objects.create(product_id=int(product[i]), qty=int(qty[i]), entree=entree)
                items.save()
        items=Entree.objects.all().annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
        context['items'] = items
        messages.success(request,"Entrée ajoutée avec succès")
        html = render(request, "stock/entree/partial/response.html", context)
        return HttpResponse(html)
      
    return render(request,'stock/entree/partial/add_response.html',context)

def add_items_form(request):
    products=Product.objects.filter(status="Activé").order_by('libelle')
    context = {
        'products': products,
        
    }
    return render(request,'stock/entree/partial/entree_items_form.html',context)


def filter_entree_by_date(request):
    if request.method == "POST":
        datestart = request.POST.get('dateStart')
        dateend = request.POST.get('dateEnd')
        items=Entree.objects.filter(dateEntree__range=[datestart, dateend]).annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
        
        context = {
            'items': items,
            'page': 'entree',  
        }
        if request.htmx:
            return render(request, 'stock/entree/partial/response.html', context)
        return render(request, 'stock/entree/entree_list.html',context)
    
    
def entree_details(request,pk):
    entree=Entree.objects.get(pk=pk)
    items=EntreeItems.objects.filter(entree=entree)
    context = {
            'items': items,
            'entree': entree,
            'page': 'entree',  
        }
    return render(request, 'stock/entree/partial/detail_response.html', context)



def entree_update_view(request, pk):
    cat=Entree.objects.get(pk=pk)
    items=Entree.objects.all().annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
    form = EntreeForm(request.POST or None, instance=cat)
    context = {
        'form': form,
        'items':items,
        'page':'entree'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, 'stock/entree/partial/response.html', context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, 'stock/entree/partial/response.html', context)
        return HttpResponse(html)

    return render(request,'stock/entree/partial/_entree_modal.html',context)



def entree_delete_item(request,pk):
    items=EntreeItems.objects.all()
    entreeItem=EntreeItems.objects.get(pk=pk)
    product=Product.objects.get(pk=entreeItem.product.pk)
    qtyAppro=entreeItem.qty
    qtyStock=product.qtyStock
    context = {
        'items':items,
        'page':'entree'
    }
    if qtyAppro > qtyStock or qtyAppro == qtyStock:
        messages.error(request, "Impossible de supprimer cette entrée car la quantité d'approvisionnement est supérieure ou égale à la quantité en stock.")
        html = render(request, 'stock/entree/partial/detail_response.html', context)
        return HttpResponse(html)
    entreeItem.delete()
    product.qtyStock -= qtyAppro
    product.save()
    # Entree.objects.get(pk=pk).adelete()
    prod=Entree.objects.all().annotate(num_product=Count("entreeitems")).order_by('-dateEntree')
    context['items'] = prod
    messages.success(request,"Entrée supprimée avec succès")
    html = render(request, 'stock/entree/partial/response.html', context)
    return HttpResponse(html)


def entree_update_item(request,pk):
    obj=EntreeItems.objects.get(pk=pk)
    oldQty=obj.qty
    form = EntreeItemsForm(request.POST or None, instance=obj)
    items=EntreeItems.objects.filter(entree=obj.entree)
    context = {
        'form': form,
        'items':items,
        'page':'entree'
    }
    if request.method == "POST":
        qty=request.POST.get('qty')
        if form.is_valid():
            product=Product.objects.get(pk=obj.product.pk)
            product.qtyStock -= oldQty
            product.qtyStock += int(qty)
            form.save()
            product.save()
            messages.success(request,"modification éffectuée avec succès")

            html = render(request, 'stock/entree/partial/detail_response.html', context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, 'stock/entree/partial/detail_response.html', context)
        return HttpResponse(html)

    return render(request,'stock/entree/partial/_entree_item_modal.html',context)



# SORTIE STOCK
def sortie_view(request):
    items=SortieStock.objects.all().annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
    products=Product.objects.filter(status="Activé").order_by('libelle')
    form=EntreeForm()
    context = {
        'items': items,
        'page': 'sortie',
        'products': products,
        
    }
    if request.htmx:
        return render(request, 'stock/sortie/partial/response.html', context)
    return render(request, 'stock/sortie/sortie_list.html',context)

def add_sortie(request):
    items=SortieStock.objects.all().annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
    products=Product.objects.filter(status="Activé").order_by('libelle')
    
    context = {
        'entrees': items,
        'products': products,
        'page': 'entree',
        
    }
    if request.method == "POST":
        libelle = request.POST.get('libelle') 
        qty= request.POST.getlist('qty') 
        product= request.POST.getlist('product') 
        motif= request.POST.getlist('motif') 
        sortie=SortieStock.objects.create(libelle=libelle)
        sortie.save()
        for i in range(len(product)):
            if product[i] == '':
                SortieStock.objects.last().delete()
                messages.error(request, "Veuillez sélectionner un produit valide.")
                html = render(request, "stock/sortie/partial/add_response.html", context)
                return HttpResponse(html)
            else:
                p=Product.objects.get(pk=product[i])
                oldQty=p.qtyStock
                if int(qty[i]) >= oldQty:
                   
                    messages.error(request,"La quantité entrée est supérieure à la quantité actuelle")
                    html = render(request, "stock/sortie/partial/add_response.html", context)
                    SortieStock.objects.last().delete()
                    return HttpResponse(html)
                items=SortieItems.objects.create(product_id=int(product[i]), qty=int(qty[i]), sortie=sortie, motif=motif[i])
                items.save()
        items=SortieStock.objects.all().annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
        context['items'] = items
        messages.success(request,"Sortie ajoutée avec succès")
        html = render(request, "stock/sortie/partial/response.html", context)
        return HttpResponse(html)
      
    return render(request,'stock/sortie/partial/add_response.html',context)

def add_sortie_items_form(request):
    products=Product.objects.filter(status="Activé").order_by('libelle')
    context = {
        'products': products,
        
    }
    return render(request,'stock/sortie/partial/sortie_items_form.html',context)


def filter_sortie_by_date(request):
    if request.method == "POST":
        datestart = request.POST.get('dateStart')
        dateend = request.POST.get('dateEnd') 
        items=SortieStock.objects.filter(dateSortie__range=[datestart, dateend]).annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
        
        context = {
            'items': items,
            'page': 'entree',  
        }
        if request.htmx:
            return render(request, 'stock/sortie/partial/response.html', context)
        return render(request, 'stock/sortie/sortie_list.html',context)
    
    
def sortie_details(request,pk):
    sortie=SortieStock.objects.get(pk=pk)
    items=SortieItems.objects.filter(sortie=sortie)
    context = {
            'items': items,
            'sortie': sortie,
            'page': 'sortie',  
        }
    return render(request, 'stock/sortie/partial/detail_response.html', context)



def sortie_update_view(request, pk):
    sortie=SortieStock.objects.get(pk=pk)
    items=SortieStock.objects.all().annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
    form = SortieForm(request.POST or None, instance=sortie)
    context = {
        'form': form,
        'items':items,
        'page':'sortie'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, 'stock/sortie/partial/response.html', context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, 'stock/sortie/partial/response.html', context)
        return HttpResponse(html)

    return render(request,'stock/sortie/partial/_sortie_modal.html',context)



def sortie_delete_item(request,pk):
    items=SortieItems.objects.all()
    entreeItem=SortieItems.objects.get(pk=pk)
    product=Product.objects.get(pk=entreeItem.product.pk)
    qtyAppro=entreeItem.qty
    qtyStock=product.qtyStock
    context = {
        'items':items,
        'page':'entree'
    }
   
    entreeItem.delete()
    product.qtyStock += qtyAppro
    product.save()
    # Entree.objects.get(pk=pk).adelete()
    prod=SortieStock.objects.all().annotate(num_product=Count("sortieitems")).order_by('-dateSortie')
    context['items'] = prod
    messages.success(request,"Sortie supprimée avec succès")
    html = render(request, 'stock/sortie/partial/response.html', context)
    return HttpResponse(html)


def sortie_update_item(request,pk):
    obj=SortieItems.objects.get(pk=pk)
    oldQty=obj.qty
    form = SortieItemsForm(request.POST or None, instance=obj)
    items=SortieItems.objects.filter(sortie=obj.sortie)
    context = {
        'form': form,
        'items':items,
        'page':'sortie'
    }
    if request.method == "POST":
        qty=request.POST.get('qty')
        if form.is_valid():
            product=Product.objects.get(pk=obj.product.pk)
            product.qtyStock += oldQty
            product.qtyStock -= int(qty)
            form.save()
            product.save()
            messages.success(request,"modification éffectuée avec succès")

            html = render(request, 'stock/sortie/partial/detail_response.html', context)
            return HttpResponse(html)
        messages.error(request, form.errors)
        html = render(request, 'stock/sortie/partial/detail_response.html', context)
        return HttpResponse(html)

    return render(request,'stock/sortie/partial/_sortie_item_modal.html',context)

    