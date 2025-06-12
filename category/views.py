from django.contrib import messages
from django.shortcuts import redirect, render
from category.forms import CategoryForm
from category.models import Categorie
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from product.models import Product


@login_required
def category_view(request):
   
    category=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm()
    context={
        'categories':category,
        'page':'category',
        'form':form,
    }
   
    if request.htmx:
        return render(request,'category/partial/response.html',context) 
    return render(request,'category/category_list.html',context)

@login_required
def category_add_view(request):
    category=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm()
    context = {
        'form': form,
        'categories': category,
        'page': 'category'
    }
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Catégorie ajoutée avec succès")
            html = render(request, "category/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, form.errors)
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return render(request, 'category/partial/_add_category_form.html', context)


@login_required
def category_update_view(request, pk):
    cat=Categorie.objects.get(pk=pk)
    categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm(request.POST or None, instance=cat)
    context = {
        'form': form,
        'categories':categories,
        'page':'category'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, "category/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)

    return render(request,'category/partial/_category_modal.html',context)

def category_delete_view(request,pk):
    cat=Categorie.objects.get(pk=pk)
    cat.status="Supprimée"
    cat.save()
    products= Product.objects.filter(categorie=cat)
    if products.exists():
        for product in products:
            product.status="Supprimé"
            product.save()
    categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,"Catégorie supprimée avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)
    
@login_required
def categorie_delete_selection(request):
    category=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm()
    context = {
        'categories': category,
        'page': 'Categorie',
        'form': form,
    }

    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une catégorie")
            html = render(request, "category/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Categorie.objects.get(pk=id)
            products= Product.objects.filter(categorie=cat)
            if products.exists():
                for product in products:
                    product.status = "Supprimé"
                    product.save()
            cat.status="Supprimée"
            cat.save()
        messages.success(request, f"{len(cat_ids)} Catégories supprimées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('classes:Categorie_list'))


def categorie_activate_selection(request):
    category=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm()
    context = {
        'categories': category,
        'page': 'Categorie',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une catégorie")
            html = render(request, "category/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Categorie.objects.get(pk=id)
            products= Product.objects.filter(categorie=cat)
            if products.exists():
                for product in products:
                    product.status = "Activé"
                    product.save()
            cat.status = "Activée"
            cat.save()
        messages.success(request, "Catégories activées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('category:category_list_view'))


def category_deactivate_selection(request):
    category=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    form = CategoryForm()
    context = {
        'categories': category,
        'page': 'Categorie',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une catégorie")
            html = render(request, "category/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Categorie.objects.get(pk=id)
            products= Product.objects.filter(categorie=cat)
            if products.exists():
                for product in products:
                    product.status = "Désactivé"
                    product.save()
            cat.status = "Désactivée"
            cat.save()
        messages.success(request, "Catégories désactivées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('category:category_list_view'))


def category_delete_all_view(request):
    count = Categorie.objects.all().count()
    Product.objects.all().update(status="Supprimé")
    Categorie.objects.all().update(status="Supprimée")
   
    categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories supprimées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)

def category_active_all_view(request):
    count = Categorie.objects.filter(status="Désactivée").count()
    Categorie.objects.filter(status="Désactivée").exclude(status="Supprimée").update(status="Activée")
    Product.objects.filter(status="Désactivé").exclude(status="Supprimé",unity__status="Supprimée").update(status="Activé")
    categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories activées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)

def category_deactive_all_view(request):
    count = Categorie.objects.filter(status="Activée").count()
    
    Categorie.objects.filter(status="Activée").exclude(status="Supprimée").update(status="Désactivée")
    Product.objects.filter(status="Activé").exclude(status="Supprimée").update(status="Désactivé")
   
    categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories activées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)
    
def show_deleted_categories(request):
    show_deleted=request.GET.get('show_deleted')
    status=False
    categories = Categorie.objects.filter(status="Supprimée").order_by('name')
    if show_deleted is None:
        status=False
        categories=Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    if show_deleted == "on":
        status=True
        categories = Categorie.objects.filter(status="Supprimée").order_by('name')
    context = {
        'categories': categories,
        'status': status,
        'page': 'category'
    }
    print("show_deleted", show_deleted)
    return render(request, "category/partial/response.html", context)
    
def category_restore_view(request, pk):
    cat = Categorie.objects.get(pk=pk)
    cat.status = "Activée"
    cat.save()
    prod=Product.objects.filter(categorie=cat).exists()
    if prod  and prod.unity.status=="Activée":
        prod.status="Activé"
        prod.save()
    categories = Categorie.objects.all().exclude(status="Supprimée").order_by('name')
    context = {
        'categories': categories,
        'page': 'category'
    }
    messages.success(request, "Catégorie restaurée avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)
 

    