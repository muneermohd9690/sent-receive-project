from django.shortcuts import render
from .models import SentItems
from .models import *
from django.http import JsonResponse
import json
from toners.models import TonerDetails,Toners

# Create your views here.
def view_sent_items(request):
    return render(request, 'view_sent_items.html')

def view_cart_items(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        cart, created = Cart.objects.get_or_create(customer= customer,complete=False)
        items= cart.cartitem_set.all()
    else:
        items=[]
    context= {'items': items}
    return render(request, 'view_cart_items.html', context)

def add_cart_items(request):

    return render(request, 'view_cart_items.html')

def update_items(request):
    data = json.loads(request.body)
    detailId = data['detailId']
    action = data['action']

    print('detailId:',detailId)
    print('action:', action)
    customer=request.user.customer
    detail=TonerDetails.objects.get(id=detailId)

    toner_printer_id=Toners.objects.get(id=detail.toner_model_id)
    printdescription=Items.objects.get(id=toner_printer_id.toner_printer.id)
    print_description=printdescription.description
    print(print_description)

    cart, created = Cart.objects.get_or_create(customer=customer,complete=False)
    cartitem,created =CartItem.objects.get_or_create(cart=cart,product=detail)

    if action=='add':
        cartitem.quantity=(cartitem.quantity+1)
    elif action=='remove':
        cartitem.quantity = (cartitem.quantity - 1)

    cartitem.save()
    if cartitem.quantity <=0:
        cartitem.delete()
    return JsonResponse('Item was added',safe=False)