from django.shortcuts import render
from .models import SentItems
from .models import *
from django.http import JsonResponse
import json
from toners.models import TonerDetails, Toners
from django.db.models import Count


def calc_total_qty():

    queryset = TonerDetails.objects.all().annotate(count=Count('issued_to'))
    for each in queryset:
        print(each.issued_to, each.count)


def view_sent_items(request):
    return render(request, 'view_sent_items.html')


def view_cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = cart.cartitem_set.all()
    else:
        items = []
    context = {'items': items}
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
    calc_total_qty()
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
