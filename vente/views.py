from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from category.models import Categorie
from product.models import Product
from utils import numFacture
from vente.models import Cart, Facture, LigneFacture, Session
from django.db.models import  Sum,Count
from django.contrib import messages

# Create your views here.
def session_list(request):
    items=Session.objects.all().order_by('login__username')
    context = {
        'items': items,
    }
    return render(request, 'vente/session/partial/response.html', context)



def session_update(request, pk):
    session = Session.objects.get(pk=pk)
    items=Session.objects.all().order_by('login__username')
    
    if session.EstOuvert == True:
        session.EstOuvert = False
        session.LastDateClose = datetime.now()
       
    else:
        session.EstOuvert = True
        session.LastDateOpen = datetime.now()
    context = {
        'items': items,
    }

    session.save()
    print("********************************************************")
    print(session.EstOuvert)
    return render(request, 'vente/session/partial/response.html', context)


def addToCart(request, pk):
    fact=Facture.objects.last()
    product = Product.objects.get(pk=pk)
    item=Cart.objects.filter(product=product).first()
    if product.qtyStock <= 0:
        messages.error(request,"La quantité est insuffisante !")
        html = render(request, "teller/partials/order_detail.html", context)
        return HttpResponse(html)
    if item is not None:
        item.qty += 1
        item.total = item.prix * item.qty
        item.save()
    else:
        Cart.objects.create(product=product, qty=1, prix=product.price, total=product.price)
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net': total - fact.remise,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def discount(request):
    fact=Facture.objects.last()
    if request.method == 'POST':
        discount = request.POST.get('discount')
        fact.remise = int(discount)
        fact.save()
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    demi=total/2
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net': total - fact.remise,
        'total_items': Cart.objects.count(),
    }
    if fact.remise >= demi:
        messages.error(request, "La remise ne doit pas dépasser 50% du total")
        html = render(request, "teller/partials/order_detail.html", context)
        return HttpResponse(html)
       
    
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)



def removeFromCart(request, pk):
    item = Cart.objects.get(pk=pk)
    item.delete()
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    fact=Facture.objects.last()
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net':net,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def clearCart(request):
    Cart.objects.all().delete()
    fact=Facture.objects.last()
    fact.remise=0
    fact.save()
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':0,
        'num_facture': fact.numFacture,
        'remise': 0,
        'net': 0,
        'total_items': 0,
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def saveCart(request):
    fact=Facture.objects.last()
    items=Cart.objects.all().order_by('pk')
    for item in items:
        LigneFacture.objects.create(facture=fact, product=item.product, qty=item.qty, prix=item.prix, total=item.total)
        fact.total += item.total
        fact.netPaye = fact.total - fact.remise
        fact.save()
    fact.vente.total += fact.netPaye
    fact.vente.save()
    Cart.objects.all().delete()
    numFacture(request.user)
    categories=Categorie.objects.all().annotate(num_product=Count("product")).filter(status="Activée").order_by('name')
    total=Facture.objects.filter(utilisateur__login=request.user).aggregate(total=Sum('netPaye'))['total']

    articles= Product.objects.all().order_by('libelle')
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
    }
    html = render(request, "teller/partials/response.html", context)
    return HttpResponse(html)

def increseQty(request, pk):
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    fact=Facture.objects.last()
    item = Cart.objects.get(pk=pk)
    qtyStock=item.product.qtyStock
    item.qty += 1
    newQty=item.qty
    item.total = item.prix * item.qty
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net': net,
        'total_items': Cart.objects.count(),
    }
    if newQty > qtyStock:
        messages.error(request,"La quantité est insuffisante !")
        html = render(request, "teller/partials/order_detail.html", context)
        return HttpResponse(html)
    item.save()
    
    
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def decreseQty(request, pk):
    item = Cart.objects.get(pk=pk)
    if item.qty > 1:
        item.qty -= 1
        item.total = item.prix * item.qty
        item.save()
    else:
        item.delete()
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    fact=Facture.objects.last()
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net': net,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def facture(request):
    fact=Facture.objects.last() 
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    
    context= {
        'items': Cart.objects.all().order_by('pk'),
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net':net,
        'date': datetime.now(),
        'user': request.user.username,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/receip_modal.html", context)
    return HttpResponse(html) 


