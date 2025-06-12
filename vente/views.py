from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.humanize.templatetags.humanize import intcomma

from cash.models import Cash, EntreeCash, SortieCash
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



def open_session(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == 'POST':
        
        dollar = request.POST.get('dollar')
        franc = request.POST.get('franc')
        date=datetime.now().date()
        if not franc:
            franc = '0'
        if not dollar:
            dollar = '0'
            
        
        cash=Cash.objects.create(
            date=date, 
            dollar=int(dollar), 
            franc=int(franc),
            estConfirme=False,
            session=session,
            )
    
        if cash:
            session.EstOuvert = True
            session.LastDateOpen = datetime.now()  
            session.save()
            context={
                'items': Session.objects.all().order_by('login__username'),
                'dollar': int(dollar),
                'franc': int(franc),
                'user': session.login.username,
                'open': True,
            }
            messages.success(request, "Vous avez ouvert la session de l': ")
            return render(request, 'vente/session/partial/response.html', context)
        session.EstOuvert = True
        session.LastDateOpen = datetime.now()  
        session.save()
       
        context={
                'items': Session.objects.all().order_by('login__username'),
                'dollar': int(dollar),
                'franc': int(franc),
                'user': session.login.username,
                'open': True,
            }
        messages.success(request, f"Vous avez ouvert la session de l'utilisateu: ")
        return render(request, 'vente/session/partial/response.html', context)
    return render(request, 'vente/session/partial/response.html', context)
        

def close_session(request, pk):
    session = Session.objects.get(pk=pk)
      
    session.EstOuvert = False
    session.LastDateClose = datetime.now()  
    session.save()
    messages.success(request, "Vous avez fermé la session de l'utilisateur: ")
    return render(request, 'vente/session/partial/response.html', {
                'items': Session.objects.all().order_by('login__username'),
                'user': session.login.username,
            })


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
    total=Facture.objects.filter(utilisateur__login=request.user,vente__dateVente=datetime.datetime.now().date()).aggregate(total=Sum('netPaye'))['total']
    articles= Product.objects.all().order_by('libelle')
    cash=Cash.objects.filter(session__login=request.user).last()
    context={
        'categories':categories,
        'articles':articles,
        'total':total,
        'cash':cash,
        'date':datetime.now().date(),
        
    }
    html = render(request, "teller/partials/response.html", context)
    return HttpResponse(html)


def increseQty(request, pk):
    item = Cart.objects.get(pk=pk)
    qtyStock=item.product.qtyStock
    if item.qty < qtyStock:
        item.qty += 1
        item.total = item.prix * item.qty
        item.save()
    else:
        messages.error(request,"La quantité est insuffisante !")
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
def change_qty_in_input(request, pk):
    fact=Facture.objects.last()
    item = Cart.objects.get(pk=pk)
    qty=request.GET.get('qty') or 1
    qtyStock=item.product.qtyStock
    item.qty =int(qty)
    newQty=item.qty
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    if newQty < qtyStock:
        item.total = item.prix * item.qty
        item.save()
        total=Cart.objects.aggregate(total=Sum('total'))['total']
        
        
    else:
        messages.error(request,"La quantité insuffisante !")
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

def deleteItemInCart(request, pk):
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
        'net': net,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)

def cancelPrint(request):
    items = Cart.objects.all()
    total=Cart.objects.aggregate(total=Sum('total'))['total']
    fact=Facture.objects.last()
    net=0
    if fact.remise > 0 and total > fact.remise:
        net = total - fact.remise
    else:
        net = total
    context= {
        'items': items,
        'total':total,
        'num_facture': fact.numFacture,
        'remise': fact.remise,
        'net': net,
        'total_items': Cart.objects.count(),
    }
    html = render(request, "teller/partials/order_detail.html", context)
    return HttpResponse(html)