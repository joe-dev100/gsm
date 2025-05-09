from django.contrib import messages
from django.shortcuts import redirect, render
from category.forms import CategoryForm
from category.models import Categorie
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def category_view(request):
   
    category=Categorie.objects.all().order_by('name')
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
    categories = Categorie.objects.all().order_by('name')
    form = CategoryForm()
    context = {
        'form': form,
        'categories': categories,
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


def category_update_view(request, pk):
    cat=Categorie.objects.get(pk=pk)
    categories=Categorie.objects.all().order_by('name')
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
    cat=Categorie.objects.get(pk=pk).delete()
   
    categories=Categorie.objects.all().order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,"Catégorie supprimée avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)
    

def categorie_delete_selection(request):
    categories = Categorie.objects.all().order_by('name')
    form = CategoryForm()
    context = {
        'categories': categories,
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
            cat.delete()
        messages.success(request, f"{len(cat_ids)} Catégories supprimées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('classes:Categorie_list'))


def categorie_activate_selection(request):
    categories = Categorie.objects.all().order_by('name')
    form = CategoryForm()
    context = {
        'categories': categories,
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
            cat.status = "Activée"
            cat.save()
        messages.success(request, "Catégories activées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('category:category_list_view'))


def category_deactivate_selection(request):
    Categories = Categorie.objects.all().order_by('name')
    form = CategoryForm()
    context = {
        'categories': Categories,
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
            cat.status = "Désactivée"
            cat.save()
        messages.success(request, "Catégories désactivées avec succès")
        html = render(request, "category/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('category:category_list_view'))


def category_delete_all_view(request):
    count = Categorie.objects.all().count()
    
    Categorie.objects.all().delete()
   
    categories=Categorie.objects.all().order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories supprimées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)

def category_active_all_view(request):
    count = Categorie.objects.filter(status="Désactivée").count()
    
    Categorie.objects.filter(status="Désactivée").update(status="Activée")
   
    categories=Categorie.objects.all().order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories activées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)

def category_deactive_all_view(request):
    count = Categorie.objects.filter(status="Activée").count()
    
    Categorie.objects.filter(status="Activée").update(status="Désactivée")
   
    categories=Categorie.objects.all().order_by('name')
    context={
        'categories':categories,
        'page':'category'
    }
    messages.success(request,f"{count} Catégories activées avec succès")
    html = render(request, "category/partial/response.html", context)
    return HttpResponse(html)
    

 

    