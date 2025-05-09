from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from product.form import ProductForm
from product.models import Product
from unity.forms import UnityForm
# Create your views here.


@login_required
def product_view(request):
    products=Product.objects.all().order_by('libelle')
    context={
        'items':products,
        'page':'products-list',
       
    }
   
    if request.htmx:
        return render(request,'product/partial/response.html',context) 
    return render(request,'product/product_list.html',context)

@login_required
def add_product(request):
    form = ProductForm()
    context = {
        'form': form,
        'page': 'product'
    }
    if request.method == "POST":
        canExpired=request.POST.get('canExpired')
        form = ProductForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get('expiried_on')
            CE=form.cleaned_data.get('canExpiried')
            if canExpired=="on" and not date:
               messages.error(request, "veuillez renseigner la date d'expiration")
               context['form'] = form
               html = render(request, "product/partial/add_response.html", context)
               return HttpResponse(html)
            
            form.save()
            messages.success(request,"Nouvel article ajouté avec succès")
            html = render(request, "product/partial/add_response.html", {'form': ProductForm()})
            return HttpResponse(html)
        messages.error(request, form.errors)
        html = render(request, "product/partial/add_response.html", context)
        return HttpResponse(html)
    if request.htmx:
        return render(request,'product/partial/add_response.html',context) 
    return render(request, 'product/add_product.html', context)

def add_new_category(request):
    form = ProductForm()
    context = {
        'form': ProductForm(),
    }
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            html = render(request, "product/partial/add_new_cat_response.html", context)
            return HttpResponse(html)
        html = render(request, "product/partial/add_new_cat_response.html", context)
        return HttpResponse(html)
    return render(request, 'product/partial/_add_product_form.html', {'form': form})

def add_new_unity(request):
    form = UnityForm()
    context = {
        'form': ProductForm(),
    }
    if request.method == "POST":
        form = UnityForm(request.POST)
        if form.is_valid():
            form.save()
            html = render(request, "product/partial/add_new_unity_response.html", context)
            return HttpResponse(html)
        html = render(request, "product/partial/add_new_unity_response.html", context)
        return HttpResponse(html)
    return render(request, 'product/partial/_add_unity_form.html', {'form': form})
   


def product_update_view(request, pk):
    prod=Product.objects.get(pk=pk)
    items=Product.objects.all().order_by('libelle')
    form = ProductForm(request.POST or None, instance=prod)
    context = {
        'form': form,
        'items':items,
        'page':'product-list'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, "product/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, "product/partial/response.html", context)
        return HttpResponse(html)

    return render(request,'product/partial/add_response.html',context)

def product_delete_view(request,pk):
    Product.objects.get(pk=pk).delete()
   
    items=Product.objects.all().order_by('libelle')
    context={
        'items':items,
        'page':'product-list'
    }
    messages.success(request,"article supprimé avec succès")
    html = render(request, "product/partial/response.html", context)
    return HttpResponse(html)
    

def product_delete_selection(request):
    items = Product.objects.all().order_by('libelle')
    form = ProductForm()
    context = {
        'items': items,
        'page': 'product-list',
        'form': form,
    }

    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins un article")
            html = render(request, "product/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Product.objects.get(pk=id)
            cat.delete()
        messages.success(request, f"{len(cat_ids)} articles supprimés avec succès")
        html = render(request, "product/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('product:product_view'))


def product_activate_selection(request):
    items = Product.objects.all().order_by('libelle')
    form = ProductForm()
    context = {
        'items': items,
        'page': 'product-list',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins un article")
            html = render(request, "product/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Product.objects.get(pk=id)
            cat.status = "Activé"
            cat.save()
        messages.success(request, " Articles activés avec succès")
        html = render(request, "product/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('product:product_view'))


def product_deactivate_selection(request):
    Items = Product.objects.all().order_by('libelle')
    form = ProductForm()
    context = {
        'items': Items,
        'page': 'product-list',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins un article")
            html = render(request, "product/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = Product.objects.get(pk=id)
            cat.status = "Désactivé"
            cat.save()
        messages.success(request, " Articles désactivés avec succès")
        html = render(request, "product/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('product:product_view'))


def product_delete_all_view(request):
    count = Product.objects.all().count()
    
    Product.objects.all().delete()
   
    items=Product.objects.all().order_by('libelle')
    context={
        'items':items,
        'page':'product-list'
    }
    messages.success(request,f"{count} Articles supprimés avec succès")
    html = render(request, "product/partial/response.html", context)
    return HttpResponse(html)

def product_active_all_view(request):
    count = Product.objects.filter(status="Désactivé").count()
    
    Product.objects.filter(status="Désactivé").update(status="Activé")
   
    items=Product.objects.all().order_by('libelle')
    context={
        'items':items,
        'page':'product-list'
    }
    messages.success(request,f"{count} Articles activés avec succès")
    html = render(request, "product/partial/response.html", context)
    return HttpResponse(html)

def product_deactive_all_view(request):
    count = Product.objects.filter(status="Activé").count()
    
    Product.objects.filter(status="Activé").update(status="Désactivé")
   
    items=Product.objects.all().order_by('libelle')
    context={
        'items':items,
        'page':'product-list'
    }
    messages.success(request,f"{count} Articles activés avec succès")
    html = render(request, "product/partial/response.html", context)
    return HttpResponse(html)
    

 