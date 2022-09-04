from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.defaultfilters import length

from .models import SentItems,Cart,CartItem
#from .models import *
from django.http import JsonResponse
import json
from toners.models import TonerDetails, Toners
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect



###                         for adding to cart                                              ###
def get_cart_items(itemsincart):
    cartitem=CartItem.objects.filter(cart=itemsincart)
    total = cartitem.count()
    return total

def listof_cartitemids():
    cartitem=CartItem.objects.all()
    print(cartitem)
    return list(CartItem.objects.all().values_list('id', flat=True))

def view_cart_items(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        itemsincart = cart.pk
        cart_total=get_cart_items(itemsincart)
        items = cart.cartitem_set.all()

    else:
        items = []

    context = {'items': items,'total':cart_total,'itemsincart':itemsincart}
    return render(request, 'view_cart_items.html', context)

def update_items(request):
    data = json.loads(request.body)
    detailId = data['detailId']
    action = data['action']
    print('detailId:', detailId)
    print('action:', action)
    customer = request.user.customer
    detail = TonerDetails.objects.get(id=detailId)
    cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
    cartitem, created = CartItem.objects.get_or_create(cart=cart, product=detail)

    if action == 'add':
        cartitem.quantity = (cartitem.quantity + 1)
    elif action == 'remove':
        cartitem.quantity = (cartitem.quantity - 1)
    cartitem.save()
    if cartitem.quantity <= 0:
        cartitem.delete()
    return JsonResponse('Item was added', safe=False)

###                         for adding to cart                                              ###

###                         for adding to dispatch                                          ###



def view_sent_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        # cartitem, created = CartItem.objects.filter(id=update_items.itemId,product_id=TonerDetails.id )
        # print(cartitem.all())
        #cartitem_total=get_cart_items(cartitem).
        #cartitem=CartItem.objects.all()
        items=CartItem.objects.all()
    else:
        items = []
    context = {'items': items}
    return render(request, 'view_sent_items.html',context)

def update_sent_items(request):
    data = json.loads(request.body)
    items = data['items']
    action = data['action']
    print('items:', items )
    print('action:', action)
    #str(eval(items.description))
    id =list(CartItem.objects.all().values_list('id', flat=True))

    cartdetail = CartItem.objects.get_or_create(product=id)
    sentitem,created= SentItems.objects.get_or_create(product=cartdetail)
    sentitem.save()
    return JsonResponse('Item was added', safe=False)




    #customer = request.user.customer
    # cartitemdetail = CartItem.objects.filter(id=itemId)
    # cartitem, created = CartItem.objects.filter(id=itemId,employee_name=employee_name)
    # print(cartitem)
    # sentitems, created = CartItem.objects.get_or_create(id=update_items.itemId )
    # sentitems.save()
    # return JsonResponse('CartItem were added to SentItems', safe=False)

def remove_from_cart(request, id):
    items = CartItem.objects.get(id=id)
    items.delete()
    messages.success(request, "Item removed from cart successfully")
    return redirect('view_cart_items')

def dispatch(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        cart.complete=True
        cart.save()
    else:
        print('User is not logged in')
    return redirect('view_sent_items')


###                           for adding to dispatch                                       ###