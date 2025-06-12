from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from vente.models import Facture, LigneFacture

# Create your views here.

def list_facture(request):
    items=Facture.objects.all().order_by('-dateFacture')
    context = {
        'items': items,
    }
    html = render(request, "facture/partial/response.html", context)
    return HttpResponse(html)


def facture_details(request, pk):
    facture=Facture.objects.get(pk=pk)
    item = LigneFacture.objects.filter(facture_id=pk).order_by('product__libelle')
    context = {
        'item': item,
        'facture': facture,
    }
    html = render(request, "facture/partial/detail.html", context)
    return HttpResponse(html)
    
def delete_facture(request, pk):
    facture=Facture.objects.get(pk=pk)
    ligne_facture=LigneFacture.objects.filter(facture_id=pk)
    items=Facture.objects.all().order_by('-dateFacture')
    context = {
        'items': items,
    }
    if request.method == 'POST':
        pw=request.POST.get('password')
        if pw == request.user.password:
            for ligne in ligne_facture:
                ligne.delete()
            facture.delete()
        else:
            messages.error("Mot de passe incorrect")
            html = render(request, "facture/partial/response.html", context)
            return HttpResponse(html)
    
        html = render(request, "facture/partial/response.html", context)
        return HttpResponse(html)


def filter_facture_by_date(request):
    if request.method == "POST":
        datestart = request.POST.get('dateStart')
        dateend = request.POST.get('dateEnd')
        items=Facture.objects.filter(dateFacture__range=[datestart, dateend]).all().order_by('-dateFacture')
        
        context = {
            'items': items,
            'page': 'entree',  
        }
        html = render(request, "facture/partial/response.html", context)
        return HttpResponse(html)