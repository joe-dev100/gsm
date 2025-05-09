from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UnityForm
from .models import UniteVente
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def unity_view(request):
   
    unity=UniteVente.objects.all().order_by('unit')
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
    uniteventes = UniteVente.objects.all().order_by('unit')
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


def unity_update_view(request, pk):
    cat=UniteVente.objects.get(pk=pk)
    uniteventes=UniteVente.objects.all().order_by('unit')
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
    cat=UniteVente.objects.get(pk=pk).delete()
   
    uniteventes=UniteVente.objects.all().order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,"Unité de vente supprimée avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)
    

def unity_delete_selection(request):
    uniteventes = UniteVente.objects.all().order_by('unit')
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
            cat.delete()
        messages.success(request, f"{len(cat_ids)} Unité de ventes supprimées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('classes:unity_list'))


def unity_activate_selection(request):
    uniteventes = UniteVente.objects.all().order_by('unit')
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
            cat.status = "Activée"
            cat.save()
        messages.success(request, "Unité de ventes activées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('unity:unity_list_view'))


def unity_deactivate_selection(request):
    UniteVentes = UniteVente.objects.all().order_by('unit')
    form = UnityForm()
    context = {
        'uniteventes': UniteVentes,
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
            cat.status = "Désactivée"
            cat.save()
        messages.success(request, "Unité de ventes désactivées avec succès")
        html = render(request, "unity/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('unity:unity_list_view'))


def unity_delete_all_view(request):
    count = UniteVente.objects.all().count()
    
    UniteVente.objects.all().delete()
   
    uniteventes=UniteVente.objects.all().order_by('unit')
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
   
    uniteventes=UniteVente.objects.all().order_by('unit')
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
   
    uniteventes=UniteVente.objects.all().order_by('unit')
    context={
        'uniteventes':uniteventes,
        'page':'unity'
    }
    messages.success(request,f"{count} Unité de ventes activées avec succès")
    html = render(request, "unity/partial/response.html", context)
    return HttpResponse(html)
    

 

    
