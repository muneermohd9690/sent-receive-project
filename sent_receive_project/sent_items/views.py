from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.template.defaultfilters import length
from django.contrib.admin.options import get_content_type_for_model
from django.utils import timezone

import toners.views
import items.views
from .models import SentItems, Cart, CartItem,Customer
# from .models import *
from django.http import JsonResponse
import json
from toners.models import TonerDetails, Toners
from items.models import ItemDetails
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .utils import calc_cart_total,get_tonerdetails_content_type_id,get_itemdetails_content_type_id
from toners.utils import calc_toner_stock_alert

ltid = []
liid = []
urlObject = ''
ctid=[]
content_type = []


###                         for adding to cart                                              ###

# def get_total_cart_items(itemsincart):
#     cartitem = CartItem.objects.filter(cart=itemsincart)
#     total = cartitem.count()
#     return total


def listof_cartitemids():
    cartitem = CartItem.objects.all()
    print(cartitem)
    return list(CartItem.objects.all().values_list('id', flat=True))


def get_list_tonerdetailsid():
    tonerdetails = TonerDetails.objects.all()
    ltid = [s.id for s in tonerdetails]
    return ltid


def get_list_itemdetailsid():
    itemdetails = ItemDetails.objects.all()
    liid = [s.id for s in itemdetails]
    return liid


def get_url_of_request(request):
    urlObject = request.META['HTTP_REFERER']
    return urlObject


def get_content_type_id():
    cartitem = CartItem.objects.all()
    ctid = [s.content_type_id for s in cartitem]  # content_type_id
    return ctid

# def get_tonerdetails_content_type_id():
#     tonerdetails_content_type = ContentType.objects.filter(model='tonerdetails')
#     for s in tonerdetails_content_type:
#         tdcid = s.id # content_type_id
#     return tdcid
#
# def get_itemdetails_content_type_id():
#     tonerdetails_content_type = ContentType.objects.filter(model='itemdetails')
#     for s in tonerdetails_content_type:
#         idcid = s.id # content_type_id
#     return idcid

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_cart_items(request):
    if request.user.is_authenticated:
        #customer = request.user.customer
        # customer, created = Customer.objects.get_or_create(user=request.user)
        # cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        # itemsincart = cart.pk
        #cart_total = get_total_cart_items(itemsincart)
        data_calc_cart_total=calc_cart_total(request)
        cart_total=data_calc_cart_total['cart_total']
        itemsincart=data_calc_cart_total['items_in_cart']
        cart=data_calc_cart_total['user_cart']
        data_calc_toner_stock_alert = calc_toner_stock_alert(request)
        toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
        toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

        # items = cart.cartitem_set.all()
        items = cart.cartitem_set.filter(selected=False, dispatched=False)

        ltid = get_list_tonerdetailsid()
        liid = get_list_itemdetailsid()
        ctid=get_content_type_id()

        data_get_tonerdetails_content_type_id = get_tonerdetails_content_type_id(request)
        tdcid = data_get_tonerdetails_content_type_id['tdcid']

        data_get_itemdetails_content_type_id = get_itemdetails_content_type_id(request)
        idcid = data_get_itemdetails_content_type_id['idcid']
        # tdcid=get_tonerdetails_content_type_id()
        # idcid = get_itemdetails_content_type_id()
    else:
        items = []
    context = {'items': items, 'total': cart_total, 'itemsincart': itemsincart, 'ltid': ltid, 'liid': liid,'urlObject':urlObject,'ctid':ctid
               ,'tdcid':tdcid,'idcid':idcid,'cart':cart,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'view_cart_items.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def update_items(request):
    data = json.loads(request.body)
    detailId = data['detailId']
    urlObject = get_url_of_request(request)
    # customer = request.user.customer
    customer, created = Customer.objects.get_or_create(user=request.user )
    cartitem = CartItem.objects.all()
    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    if 'view_tonerdetails' in urlObject :
        detail = TonerDetails.objects.get(id=detailId)
        urlid=detail.toner_model_id
        detail_q=ContentType.objects.get_for_model(detail)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        if (detail.id, detail_q.id) in joined_ids:
            messages.success(request, "Toner already in Dispatch")
        else:
            p1 = CartItem.objects.create(object_id=detail.id, cart=cart,content_type_id=int(detail_q.id))
            p1.save()
            messages.success(request, "Toner added to Dispatch")

    elif 'edit_tonerdetails_form' in urlObject :
        detail = TonerDetails.objects.get(id=detailId)
        urlid=detail.toner_model_id
        detail_q=ContentType.objects.get_for_model(detail)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        if (detail.id, detail_q.id) in joined_ids:
            messages.success(request, "Toner already in Dispatch")
        else:
            p1 = CartItem.objects.create(object_id=detail.id, cart=cart,content_type_id=int(detail_q.id))
            p1.save()
            return redirect(toners.views.edit_tonerdetails_save)
            #messages.success(request, "Toner added to Dispatch")

    elif 'view_items_details' in urlObject:
        detail = ItemDetails.objects.get(id=detailId)
        detail_q = ContentType.objects.get_for_model(detail)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        if (detail.id, detail_q.id) in joined_ids:
            messages.success(request, "Item already in Dispatch")
        else:
            p1 = CartItem.objects.create(object_id=detail.id, cart=cart, content_type_id=int(detail_q.id))
            p1.save()
            messages.success(request, "Item added to Dispatch")

    elif 'edit_item_details_form' in urlObject:
        detail = ItemDetails.objects.get(id=detailId)
        detail_q = ContentType.objects.get_for_model(detail)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        if (detail.id, detail_q.id) in joined_ids:
            messages.success(request, "Item already in Dispatch")
        else:
            p1 = CartItem.objects.create(object_id=detail.id, cart=cart, content_type_id=int(detail_q.id))
            p1.save()
            return redirect(items.views.edit_item_details_save)

    return JsonResponse('Item was added', safe=False)


###                         for adding to cart                                              ###

###                         for adding to dispatch                                          ###

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_sent_items(request):

    if request.user.is_authenticated:
        #cart=Cart.objects.filter(complete=True)
        # items = CartItem.objects.filter(cart_id__in=cart.values_list('id', flat=True))
        items = CartItem.objects.filter(dispatched=True)

        data_calc_cart_total = calc_cart_total(request)
        cart_total = data_calc_cart_total['cart_total']

        data_calc_toner_stock_alert = calc_toner_stock_alert(request)
        toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
        toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

        ltid = get_list_tonerdetailsid()
        liid = get_list_itemdetailsid()

        data_get_tonerdetails_content_type_id = get_tonerdetails_content_type_id(request)
        tdcid=data_get_tonerdetails_content_type_id['tdcid']

        data_get_itemdetails_content_type_id = get_itemdetails_content_type_id(request)
        idcid = data_get_itemdetails_content_type_id['idcid']

        #tdcid = get_tonerdetails_content_type_id() # required
        #idcid = get_itemdetails_content_type_id()  # required
    else:
        items = []
    # context = {'items': items, 'ltid': ltid, 'liid': liid,'cart':cart,'tdcid':tdcid,'idcid':idcid,"total": cart_total,
    #            "toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    context = {'items': items, 'ltid': ltid, 'liid': liid,'tdcid': tdcid, 'idcid': idcid,
               "total": cart_total,
               "toner_stock_alert": toner_stock_alert, "toner_under_fifteen": toner_under_fifteen}
    return render(request, 'view_sent_items.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def remove_from_cart(request, id):
    items = CartItem.objects.get(id=id)
    items.delete()
    messages.success(request, "Item removed from dispatch successfully")
    return redirect('view_cart_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def dispatch(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        CartItem.objects.filter(cart=cart).update(dispatched=True)
        cart.complete = True
        cart.save()
        messages.success(request, "Items Dispatched")
        return redirect('view_sent_items')
    else:
        print('User is not logged in')
    return redirect('view_sent_items')

###                           for adding to dispatch                                       ###

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def bulk_update_items(request):
    if request.method == 'POST':
        detail_ids = request.POST.getlist('selected_ids[]', [])
        urlObject = get_url_of_request(request)
        customer, created = Customer.objects.get_or_create(user=request.user )
        cartitem = CartItem.objects.all()
        joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
        itemcount=0
        tonercount=0
        if 'view_tonerdetails' in urlObject :
            for detailId in detail_ids:
                tonercount+= 1
                detail = TonerDetails.objects.get(id=detailId)
                urlid=detail.toner_model_id
                detail_q=ContentType.objects.get_for_model(detail)
                cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
                if (detail.id, detail_q.id) in joined_ids:
                    messages.success(request, "Toner already in Dispatch")
                else:
                    p1 = CartItem.objects.create(object_id=detail.id, cart=cart,content_type_id=int(detail_q.id))
                    p1.save()
                    toner_count_message = f"{str(tonercount)} Toners added to Dispatch."
                    messages.success(request, toner_count_message)


        elif 'view_items_details' in urlObject:
            for detailId in detail_ids:
                itemcount+=1
                detail = ItemDetails.objects.get(pk=detailId)
                detail_q = ContentType.objects.get_for_model(detail)
                cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
                if (detail.id, detail_q.id) in joined_ids:
                    messages.success(request, "Item already in Dispatch")
                else:
                    p1 = CartItem.objects.create(object_id=detail.id, cart=cart, content_type_id=int(detail_q.id))
                    p1.save()
                    item_count_message = f"{str(itemcount)} Items added to Dispatch."
                    messages.success(request, item_count_message)

        return JsonResponse('Item was added', safe=False)


###                         for bulk adding to dispatch                                              ###

###                         for removing selected items from dispatch                                              ###
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def select_remove_from_cart(request):
    if request.method == "POST":
        items_ids = request.POST.getlist('selected_ids[]')
        for id in items_ids:
            items = CartItem.objects.get(pk=id)
            items.delete()
    return JsonResponse('Item was removed', safe=False)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def select_dispatch(request):
    if request.user.is_authenticated and request.method == "POST":
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        selected_item_ids = request.POST.getlist('selected_ids[]')
        CartItem.objects.filter(id__in=selected_item_ids, cart=cart).update(selected=True, dispatched=True)
        # for id in selected_item_ids:
        #     cartitems=CartItem.objects.get(pk=id)
        #     print(cartitems.cart_id)
        if cart.cartitem_set.filter(selected=False).count() == 0:
            cart.complete = True
            cart.save()
        return JsonResponse('Item was dispatched', safe=False)
    else:
        print('User is not logged in')
    return redirect('view_sent_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def return_to_store(request, id):
    # items = CartItem.objects.get(id=id)
    try:
        cart_item = CartItem.objects.get(id=id)
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found")
        return redirect('view_sent_items')
    # cart_item.delete()
    toner_details = cart_item.tonerdetails.first()
    if toner_details:
        # Update the TonerDetails fields

        toner_details.status = 'In-Stock'
        toner_details.issued_to_id = '31'
        toner_details.employee_name = 'returned from dispatch'
        toner_details.employee_designation = 'returned from dispatch'
        toner_details.date_dispatched = timezone.now()

        # Save the changes to TonerDetails
        toner_details.save()

    else:
        # Check if the CartItem is associated with ItemDetails
        item_details = cart_item.itemdetails.first()

        if item_details:
            # Update the ItemDetails fields
            item_details.status = 'In-Stock'
            item_details.issued_to_id = '31'
            item_details.employee_name = 'returned from dispatch'
            item_details.employee_designation = 'returned from dispatch'
            item_details.date_dispatched = timezone.now()
            item_details.save()
    cart_item.delete()
    messages.success(request, "Item returned successfully")
    return redirect('view_sent_items')