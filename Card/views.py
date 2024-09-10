from django.shortcuts import render, get_object_or_404
from .card import Card
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cardSummery(request):
    card = Card(request)
    card_products = card.get_products
    quantities = card.get_quantity
    totals = card.cardTotal()
    return render(request, 'card/cardsummery.html', {'card_products': card_products, 'quantities':quantities, 'totals':totals})

def cardAdd(request):
    #Get the card
    card = Card(request)
    #Test for POST
    if request.POST.get('action')=='post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to session
        card.add(product=product, quantity=product_qty)
        

        #Get card Quantity
        card_quantity = card.__len__()

        #Retun response
        #response = JsonResponse({'Product Name:': product.name})
        messages.success(request, ('Product added to your card...'))
        return JsonResponse({'qty': card_quantity})
        
    
def cardUpdate(request):
    card = Card(request)
    if request.POST.get('action')=='post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        card.update(product=product_id, quantity=product_qty)
        messages.success(request, ('Your card has been updated.'))
        return JsonResponse({'qty': product_qty})
    


def cardDelete(request):
    card = Card(request)
    if request.POST.get('action')=='post':
        product_id = request.POST.get('product_id')
        card.delete(product=product_id)
        messages.success(request, ('Product has been removed from you card succesfully!'))
        return JsonResponse({})