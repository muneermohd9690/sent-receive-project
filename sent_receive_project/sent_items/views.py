import calendar

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.template.defaultfilters import length
from django.contrib.admin.options import get_content_type_for_model
from django.utils import timezone
from datetime import datetime
import toners.views
import items.views
from .models import SentItems, Cart, CartItem,Customer
from django.utils.dateformat import format as dj_format
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
from django.http import JsonResponse
from django.db.models import Q
from django.utils.dateformat import format
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.contrib.contenttypes.prefetch import GenericPrefetch

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
    items_data = []

    if request.user.is_authenticated:
        #cart=Cart.objects.filter(complete=True)
        # items = CartItem.objects.filter(cart_id__in=cart.values_list('id', flat=True))
        # Get ContentType references
        itemdetails_ct = ContentType.objects.get_for_model(ItemDetails)
        tonerdetails_ct = ContentType.objects.get_for_model(TonerDetails)


        # Optimize related object queries
        itemdetails_qs = ItemDetails.objects.select_related('model_no', 'issued_to')
        tonerdetails_qs = TonerDetails.objects.select_related('toner_model__toner_printer', 'issued_to')

        # items = CartItem.objects.filter(dispatched=True)
        items = CartItem.objects.filter(dispatched=True).select_related('cart','content_type').order_by('-date_added')
        for item in items:
            content_object = item.content_object
            if item.content_type == tonerdetails_ct:
                items_data.append({
                    'id': item.id,
                    'type': 'toner',
                    'date_dispatched': content_object.date_dispatched,
                    'issued_to': content_object.issued_to,
                    'description': content_object.toner_model.toner_printer.description,
                    'model_no': content_object.toner_model.toner_printer.model_no,
                    'toner_model': content_object.toner_model.toner_model,
                    'employee_name': content_object.employee_name,
                    'content_object': content_object,
                    'content_type': item.content_type,
                })
            elif item.content_type == itemdetails_ct:
                items_data.append({
                    'id': item.id,
                    'type': 'item',
                    'date_dispatched': content_object.date_dispatched,
                    'issued_to': content_object.issued_to,
                    'description': content_object.model_no.description,
                    'model_no': content_object.model_no.model_no,
                    'serial_no': content_object.serial_no,
                    'employee_name': content_object.employee_name,
                    'content_object': content_object,
                    'content_type': item.content_type,
                })
        data_calc_cart_total = calc_cart_total(request)
        cart_total = data_calc_cart_total['cart_total']

        data_calc_toner_stock_alert = calc_toner_stock_alert(request)
        toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
        toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

        ltid = get_list_tonerdetailsid()
        liid = get_list_itemdetailsid()
        tdcid = itemdetails_ct.id
        idcid = tonerdetails_ct.id
        # data_get_tonerdetails_content_type_id = get_tonerdetails_content_type_id(request)
        # tdcid=data_get_tonerdetails_content_type_id['tdcid']
        #
        # data_get_itemdetails_content_type_id = get_itemdetails_content_type_id(request)
        # idcid = data_get_itemdetails_content_type_id['idcid']

        #tdcid = get_tonerdetails_content_type_id() # required
        #idcid = get_itemdetails_content_type_id()  # required
    else:
        items_data = []

    context = {'items_data': items_data,
               'ltid': ltid,
               'liid': liid,
               'tdcid': tdcid,
               'idcid': idcid,
               "total": cart_total,
               "toner_stock_alert": toner_stock_alert,
               "toner_under_fifteen": toner_under_fifteen}
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
        return redirect('sent_items_ajax')
    else:
        print('User is not logged in')
    return redirect('sent_items_ajax')

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
    # return redirect('view_sent_items')
    return redirect('sent_items_ajax')

def build_search_filters(search_value):
    filters = (
        Q(tonerdetails__toner_model__toner_model__icontains=search_value) |
        Q(tonerdetails__employee_name__icontains=search_value) |
        Q(tonerdetails__issued_to__name__icontains=search_value) |
        Q(itemdetails__serial_no__icontains=search_value) |
        Q(itemdetails__model_no__description__icontains=search_value) |
        Q(itemdetails__model_no__model_no__icontains=search_value) |
        Q(itemdetails__issued_to__name__icontains=search_value) |
        Q(itemdetails__employee_name__icontains=search_value)
    )

    search_lower = search_value.lower()

    # Try parsing full date like "April 21, 2025"
    try:
        parsed_date = datetime.strptime(search_value.strip(), '%B %d, %Y')
        filters |= Q(itemdetails__date_dispatched__date=parsed_date.date())
        filters |= Q(tonerdetails__date_dispatched__date=parsed_date.date())

    except ValueError:
        pass

    # Year check
    if search_value.isdigit() and len(search_value) == 4:
        year = int(search_value)
        if year > 2000:
            filters |= Q(itemdetails__date_dispatched__year=search_value)
            filters |= Q(tonerdetails__date_dispatched__year=search_value)


    # Day check
    if search_value.isdigit() and 1 <= len(search_value) <= 2:
        day = int(search_value)
        if 1 <= day <= 31:
            filters |= Q(itemdetails__date_dispatched__day=day)
            filters |= Q(tonerdetails__date_dispatched__day=day)


    # Month name/abbr check
    for i in range(1, 13):
        if search_lower in calendar.month_name[i].lower() or search_lower in calendar.month_abbr[i].lower():
            filters |= Q(itemdetails__date_dispatched__month=i)
            filters |= Q(tonerdetails__date_dispatched__month=i)

            break

    return filters


def sent_items_ajax(request):
    toner_data = calc_toner_stock_alert(request)
    toner_stock_alert = toner_data['toner_stock_alert_count']
    toner_under_fifteen = toner_data['tonerstock']
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']

    if request.method == 'POST':
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '').strip()

        qs = CartItem.objects.filter(dispatched=True).select_related('cart', 'content_type').prefetch_related('content_object').order_by('-date_dispatched')

        if search_value:
            filters = build_search_filters(search_value)
            qs = qs.filter(filters)

        total_records = len(qs) if isinstance(qs, list) else qs.count()
        paginated_qs = qs[start:start + length]

        data = []
        for idx, item in enumerate(paginated_qs, start=start + 1):
            obj = item.content_object
            model_type = item.content_type.model

            # Initialize fields
            description = model_no = received_by = send_to = serial_no = ''
            send_date = None
            item_type = 'unknown'

            if model_type == 'tonerdetails':
                toner = obj.toner_model
                description = f"{toner.toner_printer.description} toner" if toner and toner.toner_printer else ''
                model_no = toner.toner_printer.model_no if toner and toner.toner_printer else ''
                received_by = obj.employee_name
                send_to = obj.issued_to.name if obj.issued_to else ''
                serial_no = toner.toner_model
                send_date = obj.date_dispatched
                item_type = 'toner'

            elif model_type == 'itemdetails':
                item_master = obj.model_no
                description = item_master.description if item_master else ''
                model_no = item_master.model_no if item_master else ''
                received_by = obj.employee_name
                send_to = obj.issued_to.name if obj.issued_to else ''
                serial_no = obj.serial_no or ''
                send_date = obj.date_dispatched
                item_type = 'hardware'

            action_html = f'''
                <a class="btn btn-danger open-return-modal"
                   data-id="{item.id}"
                   data-url="/sent_items/sent_items_ajax/return_to_store/{item.id}"
                   data-employee="{received_by}"
                   data-description="{description}"
                   data-modelno="{model_no}"
                   data-serial="{serial_no}"
                   data-toner="{description if item_type == 'toner' else ''}"
                   data-toner-model="{serial_no if item_type == 'toner' else ''}"
                   data-toner-printer="{model_no if item_type == 'toner' else ''}"
                   data-type="{item_type}"
                   data-bs-toggle="modal"
                   data-bs-target="#returnToStoreModal"
                   title="Return to Store">
                   <i class="fas fa-warehouse"></i>
                </a>
            '''

            data.append({
                'no': idx,
                'send_date': format(send_date, 'F j, Y') if send_date else '',
                'send_to': send_to,
                'product_description': description,
                'model_no': model_no,
                'serial_no': serial_no,
                'received_by': received_by,
                'action': action_html
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        })

    return render(request, 'lazy_loading.html', {
        "toner_stock_alert": toner_stock_alert,
        "toner_under_fifteen": toner_under_fifteen,
        "total": cart_total
    })