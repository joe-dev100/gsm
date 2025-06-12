from django.contrib import messages
from django.shortcuts import redirect, render

from product.models import Product
from .forms import UnityForm
from .models import UniteVente
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def unity_view(request):
   
    unity=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm()
    context={
        'uniteventes':unity,
        'page':'unity',
        'form':form,
    }
   
    if request.htmx:
        return render(request,'unity/partial/response.html',context) 
    return render(request,'unity/unity_list.html',context)

@login_required
def unity_add_view(request):
    uniteventes = UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm()
    context = {
        'form': form,
        'uniteventes': uniteventes,
        'page': 'unity'
    }
    if request.method == "POST":
        form = UnityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Unité de vente ajoutée avec succès")
            html = render(request, "unity/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, form.errors)
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return render(request, 'unity/partial/_add_unity_form.html', context)

#TODO: fix delete selection
def unity_update_view(request, pk):
    cat=UniteVente.objects.get(pk=pk)
    uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm(request.POST or None, instance=cat)
    context = {
        'form': form,
        'uniteventes':uniteventes,
        'page':'unity'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, "unity/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)

    return render(request,'unity/partial/_unity_modal.html',context)

def unity_delete_view(request,pk):
    cat=UniteVente.objects.get(pk=pk)
    cat.status="Supprimée"
    cat.save()
    products= Product.objects.filter(unity=cat)
    if products.exists():
        for product in products:
            product.status="Supprimé"
            product.save()
   
    uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,"Unité de vente supprimée avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)
    

def unity_delete_selection(request):
    uniteventes = UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm()
    context = {
        'uniteventes': uniteventes,
        'page': 'UniteVente',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        print(cat_ids)
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "unity/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = UniteVente.objects.get(pk=id)
            products= Product.objects.filter(unity=cat)
            if products.exists():
                for product in products:
                    product.status = "Supprimé"
                    product.save()
            cat.status="Supprimée"
            cat.save()
        messages.success(request, f"{len(cat_ids)} Unité de ventes supprimées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('classes:unity_list'))


def unity_activate_selection(request):
    uniteventes = UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm()
    context = {
        'uniteventes': uniteventes,
        'page': 'UniteVente',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "unity/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = UniteVente.objects.get(pk=id)
            products= Product.objects.filter(unit=cat)
            if products.exists():
                for product in products:
                    product.status = "Activé"
                    product.save()
            cat.status = "Activée"
            cat.save()
        messages.success(request, "Unité de ventes activées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('unity:unity_list_view'))


def unity_deactivate_selection(request):
    UniteVentes = UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    form = UnityForm()
    context = {
        'uniteventes': UniteVentes,
        'page': 'UniteVente',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        print(cat_ids)
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "unity/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = UniteVente.objects.get(pk=id)
            cat.status = "Désactivée"
            cat.save()
        messages.success(request, "Unité de ventes désactivées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('unity:unity_list_view'))


def unity_delete_all_view(request):
    count = UniteVente.objects.all().count()
    Product.objects.all().update(status="Supprimé")
    UniteVente.objects.all().update(status="Supprimée")
   
    uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,f"{count} Unité de ventes supprimées avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)

def unity_active_all_view(request):
    count = UniteVente.objects.filter(status="Désactivée").count()
    
    UniteVente.objects.filter(status="Désactivée").update(status="Activée")
    Product.objects.all().exclude(categorie__status="Supprimée", status="Supprimé").update(status="Activé")
    uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,f"{count} Unité de ventes activées avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)

def unity_deactive_all_view(request):
    count = UniteVente.objects.filter(status="Activée").count()
    
    UniteVente.objects.filter(status="Activée").update(status="Désactivée")
    Product.objects.all().update(status="Désactivé")
    uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,f"{count} Unité de ventes activées avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)
    
def show_deleted_unity(request):
    show_deleted=request.GET.get('show_deleted')
    status=False
    uniteventes = UniteVente.objects.filter(status="Supprimée").order_by('unit')
    if show_deleted is None:
        status=False
        uniteventes=UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    if show_deleted == "on":
        status=True
        uniteventes = UniteVente.objects.filter(status="Supprimée").order_by('unit')
    context = {
        'uniteventes': uniteventes,
        'status': status,
        'page': 'unity'
    }
    print("show_deleted", show_deleted)
    return render(request, "unity/partial/response.html", context)
    
def unity_restore_view(request, pk):
    cat = UniteVente.objects.get(pk=pk)
    cat.status = "Activée"
    cat.save()
    prod=Product.objects.filter(unity=cat).exists()
    if prod  and prod.categorie.status=="Activée":
        prod.status="Activé"
        prod.save()
    uniteventes = UniteVente.objects.all().exclude(status="Supprimée").order_by('unit')
    context = {
        'uniteventes': uniteventes,
        'page': 'unity'
    }
    messages.success(request, "Unité de vente restaurée avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)
 

    
 

    
