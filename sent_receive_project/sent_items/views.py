from django.shortcuts import render, redirect
from .models import SentItems,Cart,CartItem
#from .models import *
from django.http import JsonResponse
import json
from toners.models import TonerDetails, Toners
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect


def get_cart_items(cart):
    cartitems = cart.cartitem_set.all()
    total = sum([item.quantity for item in cartitems])
    return total



def view_sent_items(request):
    return render(request, 'view_sent_items.html')


def view_cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        cart_total=get_cart_items(cart)
        items = cart.cartitem_set.all()
    else:
        items = []
    context = {'items': items,'total':cart_total}
    return render(request, 'view_cart_items.html', context)


def add_cart_items(request):
    return render(request, 'view_cart_items.html')


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

def dispatch(request):
    if request.method == "POST":
        sentitems = SentItems()
        received_by = request.POST.get("employee_name")
        SentItems_model =SentItems(received_by=received_by)
        SentItems.save(received_by)
        return redirect('view_sent_items')
    else:
        return redirect('view_sent_items')