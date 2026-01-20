import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, redirect

import calendar
from contracts.models import Contracts
from .models import Items, ItemDetails, Prosecutions,CartItem
from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import forms
import pandas as pd
import excel
from django.core.files.storage import FileSystemStorage, default_storage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import json
from datetime import datetime
from django.core.paginator import Paginator
from sent_items.utils import calc_cart_total
from toners.utils import  calc_toner_stock_alert
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile, File
from django.utils.text import slugify
from django.utils.timezone import now
import os
from django.conf import settings


# def calc_total_qty():
#     for item in Items.objects.annotate(itemdetails_count=Count('itemdetails')):
#         item.total_qty = item.itemdetails_count
#         item.save(update_fields=['total_qty'])
#
#
# def calc_remaining_qty():
#     filters = Q(itemdetails__status="In-Stock")
#     for item in Items.objects.all().annotate(itemdetails_count=Count('itemdetails', filters)):
#         item.remaining_qty = item.itemdetails_count
#         # TonerDetails.objects.bulk_create([TonerDetails(toner_model=toner_model) for i in range(int(quantity))])
#         item.save(update_fields=['remaining_qty'])
#         # Toners.objects.bulk_update(tonerdetails_count,['remaining_qty'])

def calc_total_qty():
    """Recalculates total quantity for all Hardware Items."""
    for item in Items.objects.all():
        # Direct count from the database for this specific item
        actual_count = ItemDetails.objects.filter(model_no=item).count()
        item.total_qty = actual_count
        item.save(update_fields=['total_qty'])

def calc_remaining_qty():
    """Recalculates In-Stock quantity for all Hardware Items."""
    for item in Items.objects.all():
        # Direct count of items where status is In-Stock
        in_stock_count = ItemDetails.objects.filter(model_no=item, status="In-Stock").count()
        item.remaining_qty = in_stock_count
        item.save(update_fields=['remaining_qty'])

def find_item_model_id(itemdetails_id):
    global item_model_id
    item_model=ItemDetails.objects.filter(id=itemdetails_id)
    for i in item_model:
        item_model_id=i.model_no_id
    return item_model_id

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def items(request):
    return HttpResponse("this is for the items page")

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_items(request):
    #items = Items.objects.all()
    itemdetails = ItemDetails.objects.all()
    calc_remaining_qty()
    items = Items.objects.all().order_by('model_no')
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context={"total":cart_total,"items":items,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'view_items.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_items_details(request, id):
    itemdetails = ItemDetails.objects.filter(model_no=id)
    cartitem = CartItem.objects.all()
    contracts = Contracts.objects.all()
    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    itemdetails_content_type = ContentType.objects.get(app_label='items', model='itemdetails')
    content_type_id = itemdetails_content_type.id
    joined_ids = json.dumps(joined_ids)

    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"itemdetails": itemdetails,
               "joined_ids": joined_ids,
               "content_type_id": content_type_id,
               "item_id":id,
               "total":cart_total,
               "toner_stock_alert":toner_stock_alert,
               "toner_under_fifteen":toner_under_fifteen,
               "contracts":contracts,}
    return render(request, 'view_items_details.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_items(request):
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context={"total": cart_total,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'add_items.html',context)


# this is where items are added.modelmo,description,quantity should be calculated after item_details_save
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_items_save(request):
    if request.method == "POST":
        if request.POST['model_no'].strip()=="":
            messages.error(request, "Model Number is empty")
            return redirect('add_items')
        model_no = request.POST['model_no'].strip()

        if Items.objects.filter(model_no=model_no).exists():
            messages.error(request, "Model Number already exists")
            return redirect('add_items')
        elif request.POST.get('model_no') or request.POST.get('description'):
             items = Items()
             items.model_no = request.POST.get("model_no").strip()
             items.description = request.POST.get("description").strip()
             items.save()
             messages.success(request,"Item Added Successfully")
             return redirect('view_items')
    else:
        return redirect('view_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_items_details(request):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
    contracts=Contracts.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context={"prosecutions": prosecutions,"contracts":contracts, "items": items,"total":cart_total,
             "toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen,
             "status": ItemDetails.STATUS}
    return render(request, 'add_items_details.html', context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_items_details_save(request):
    if request.method == "POST":
        serial_no = request.POST.get("serial_no").strip()

        # Check if the checkbox is checked
        if request.POST.get("na_checkbox"):
            serial_no = None  # Set serial number to None if NA checkbox is checked
        else:
            # Check if serial number is empty
            if not serial_no:
                messages.error(request, "Please enter a serial number.")
                return redirect('add_items_details')
        if serial_no is not None:  # Check for existing serial number only if it's not None
            # Check if the serial number already exists
            if ItemDetails.objects.filter(serial_no=serial_no).exists():
                existing_item = ItemDetails.objects.get(serial_no=serial_no)
                model_name = existing_item.model_no.model_no  # Assuming model_no has a 'name' field
                message = f"Serial number {serial_no} already exists. Associated model: {model_name}."
                # serial_number_error = f"{str(serial_number_count)} serial numbers already exists in Database."
                messages.error(request, message)
                return redirect('view_items')



        model_no_id = request.POST.get("model_no").strip()
        model_no = Items.objects.get(id=model_no_id)

        tag_no = request.POST.get("tag_no").strip()
        room_tag = request.POST.get("room_tag").strip()

        name_id = request.POST.get("issued_to").strip()
        issued_to = Prosecutions.objects.get(id=name_id)

        contract_id = request.POST.get("lpo_no").strip()
        lpo_no = Contracts.objects.get(id=contract_id)

        employee_name = request.POST.get("employee_name").strip()
        employee_designation = request.POST.get("employee_designation").strip()

        if 'pdf_file' in request.FILES:
            new_pdf_file = request.FILES['pdf_file']
            today_date = now().strftime("%Y-%m-%d")  # Get today's date in YYYY-MM-DD format
            employee_name_slug = slugify(employee_name, allow_unicode=True)
            new_filename = f"{employee_name_slug}_signed_{today_date}.pdf"
            # Save the uploaded file with the constructed filename
            with open(f'pdfs/itemdetails/{new_filename}', 'wb+') as destination:
                 for chunk in new_pdf_file.chunks():
                    destination.write(chunk)
            # Assign the filename to the pdf_file field

            pdf_file_path = f"pdfs/itemdetails/{new_filename}"
        else:
            pdf_file_path = None

        status = request.POST.get("status")

        # Save item details if serial number does not exist
        ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no, tag_no=tag_no, room_tag=room_tag,
                                        issued_to=issued_to, employee_name=employee_name,lpo_no=lpo_no,
                                        employee_designation=employee_designation,pdf_file=pdf_file_path, status=status)
        ItemDetails_model.save()
        messages.success(request, "Item Details Added Successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_items')
    else:
        return redirect('view_items')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_items(request):
    items = Items.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"items": items,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'view_items.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_items_form(request, id):
    items = Items.objects.get(id=id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total, "items": items,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_items_form.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_items_save(request):
    if request.method == "POST":
        items_id = request.POST.get("items_id")
        model_no = request.POST.get("model_no").strip()
        description = request.POST.get("description").strip()
        total_qty = request.POST.get("total_qty")
        Items_model = Items(id=items_id, model_no=model_no, description=description, total_qty=total_qty)
        Items_model.save()
        messages.success(request, "Item Edited Successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_items')
    else:
        return redirect('view_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_items_delete(request, id):
    items = Items.objects.get(id=id)
    items.delete()
    messages.success(request, "Item Deleted Successfully")
    return redirect('view_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
# def edit_item_details(request):
    # itemdetails = ItemDetails.objects.all()
    # items = Items.objects.all()
    # prosecutions=Prosecutions.objects.all()
    # contracts=Contracts.objects.all()
    # data_calc_cart_total = calc_cart_total(request)
    # cart_total = data_calc_cart_total['cart_total']
    # data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    # toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    # toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    # context = {"total": cart_total,"itemdetails": itemdetails,"toner_stock_alert":toner_stock_alert,"items": items,
    #            "toner_under_fifteen":toner_under_fifteen,"prosecutions":prosecutions
    #            ,"contracts":contracts,"status": ItemDetails.STATUS}
    # return render(request, 'edit_item_details.html', context)
def edit_item_details(request):
    itemdetails = ItemDetails.objects.all()
    items = Items.objects.all()
    prosecutions=Prosecutions.objects.all()
    contracts=Contracts.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"itemdetails": itemdetails,"toner_stock_alert":toner_stock_alert,"items": items,
               "toner_under_fifteen":toner_under_fifteen,"prosecutions":prosecutions
               ,"contracts":contracts,"status": ItemDetails.STATUS}
    return render(request, 'edit_item_details.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def search_dropdown_options(request):
    model = request.GET.get('model')
    query = request.GET.get('q', '')
    results = []

    if model == 'items':
        queryset = Items.objects.filter(model_no__icontains=query)[:20]
        results = [{'id': item.id, 'text': item.model_no} for item in queryset]
    elif model == 'prosecutions':
        queryset = Prosecutions.objects.filter(name__icontains=query)[:20]
        results = [{'id': prosecution.id, 'text': prosecution.name} for prosecution in queryset]
    elif model == 'contracts':
        queryset = Contracts.objects.filter(lpo_no__icontains=query)[:20]
        results = [{'id': contract.id, 'text': contract.lpo_no} for contract in queryset]

    return JsonResponse({'results': results})

def build_search_filters(search_value):
    filters = (

        Q(serial_no__icontains=search_value) |
        # Q(model_no__description__icontains=search_value) |
        Q(model_no__model_no__icontains=search_value) |
        Q(tag_no__icontains=search_value) |
        Q(room_tag__icontains=search_value) |
        Q(issued_to__name__icontains=search_value) |
        Q(employee_name__icontains=search_value) |
        Q(employee_designation__icontains=search_value) |
        Q(lpo_no__lpo_no__icontains=search_value)
    )

    search_lower = search_value.lower()

    # Try parsing full date like "April 21, 2025"
    try:
        parsed_date = datetime.strptime(search_value.strip(), '%B %d, %Y')
        filters |= Q(date_dispatched__date=parsed_date.date())
    except ValueError:
        pass

    # Year check
    if search_value.isdigit() and len(search_value) == 4:
        year = int(search_value)
        if year > 2000:
            filters |= Q(date_dispatched__year=search_value)


    # Day check
    if search_value.isdigit() and 1 <= len(search_value) <= 2:
        day = int(search_value)
        if 1 <= day <= 31:
            filters |= Q(date_dispatched__day=day)


    # Month name/abbr check
    for i in range(1, 13):
        if search_lower in calendar.month_name[i].lower() or search_lower in calendar.month_abbr[i].lower():
            filters |= Q(date_dispatched__month=i)

            break

    return filters

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def item_details_datatable(request):
    toner_data = calc_toner_stock_alert(request)
    toner_stock_alert = toner_data['toner_stock_alert_count']
    toner_under_fifteen = toner_data['tonerstock']
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    # Extract DataTables parameters
    if request.method == 'POST':
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '').strip()
        order_column = int(request.POST.get('order[0][column]', 5))
        order_dir = request.POST.get('order[0][dir]', 'desc')

        # Map DataTables column index to model fields
        columns = [
            'model_no__model_no',  # model_no.model_no
            'serial_no',
            'tag_no',
            'room_tag',
            'issued_to__name',  # issued_to.name
            'date_dispatched',
            'employee_name',
            'employee_designation',
            'lpo_no__lpo_no',  # lpo_no.lpo_no
        ]
        order_field = columns[order_column]
        if order_dir == 'desc':
            order_field = '-' + order_field

        queryset = ItemDetails.objects.select_related('model_no', 'issued_to', 'lpo_no')
        total_records = queryset.count()

        # Apply search
        if search_value:
            filters = build_search_filters(search_value)
            queryset = queryset.filter(filters)


        filtered_records = queryset.count()
        queryset = queryset.order_by(order_field)[start:start + length]

        # Prepare data for DataTables
        data = []
        for detail in queryset:
            data.append({
                'model_no': detail.model_no.model_no if detail.model_no else '',
                'serial_no': detail.serial_no or '',
                'tag_no': detail.tag_no or '',
                'room_tag': detail.room_tag or '',
                'issued_to': detail.issued_to.name if detail.issued_to else '',
                'date_dispatched': detail.date_dispatched.strftime('%B %d, %Y') if detail.date_dispatched else '',
                'employee_name': detail.employee_name or '',
                'employee_designation': detail.employee_designation or '',
                'lpo_no': detail.lpo_no.lpo_no if detail.lpo_no else '',
                'action': f'<button type="button" class="btn btn-warning" onclick="openModal(\'{detail.pk}\')"><i class="fas fa-edit"></i></button>',
                'id': str(detail.pk)
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })
    return render(request, 'edit_item_details.html', {
        "toner_stock_alert": toner_stock_alert,
        "toner_under_fifteen": toner_under_fifteen,
        "total": cart_total
    })


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_item_details_form(request, id):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
    contracts = Contracts.objects.all()
    #itemdetails = ItemDetails.objects.get(id=id)
    detail = ItemDetails.objects.get(id=id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    cartitem = CartItem.objects.all()
    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    itemdetails_content_type = ContentType.objects.get(app_label='items', model='itemdetails')
    content_type_id = itemdetails_content_type.id
    joined_ids = json.dumps(joined_ids)
    context = {"total": cart_total, "detail": detail, "items": items,"toner_stock_alert":toner_stock_alert,
               "joined_ids":joined_ids,"prosecutions": prosecutions,"content_type_id":content_type_id
               ,"contracts":contracts,"toner_under_fifteen":toner_under_fifteen, "status": ItemDetails.STATUS}
    return render(request, 'edit_item_details_form.html',context)


# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url="login")
# def edit_item_details_modal(request):
#     detail_id = request.GET.get('detail_id')
#     items = Items.objects.all()
#     prosecutions = Prosecutions.objects.all()
#     contracts=Contracts.objects.all()
#
#     # Fetch details from the database based on detail_id
#     try:
#         detail = ItemDetails.objects.get(pk=detail_id)
#         # print(f"Model Number: {detail.model_no}, Issued to: {detail.issued_to}")
#     except ItemDetails.DoesNotExist:
#         print(f"ItemDetails with id={detail_id} does not exist.")
#
#     # Render a template or return JSON data depending on your needs
#     context = {'detail': detail, 'items': items, 'prosecutions': prosecutions,'contracts': contracts, "status": ItemDetails.STATUS}
#     return render(request, 'edit_item_details_modal.html', context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_item_details_modal(request):
    detail_id = request.GET.get('detail_id')
    prosecutions = Prosecutions.objects.all()
    contracts = Contracts.objects.all()
    items = Items.objects.all()

    try:
        detail = ItemDetails.objects.select_related('model_no', 'issued_to', 'lpo_no').get(pk=detail_id)
    except ItemDetails.DoesNotExist:

        return JsonResponse({'error': 'Item not found'}, status=404)

    context = {
        'detail': detail,
        'items':items,
        'status': ItemDetails.STATUS,
        'prosecutions':prosecutions,
        'contracts':contracts

    }
    return render(request, 'edit_item_details_modal.html', context)


# def edit_item_details_save(request):
#     if request.method == "POST":
#         itemdetails_id = request.POST.get("detail_id")
#
#         # Retrieve existing ItemDetails instance
#         item_details_model = get_object_or_404(ItemDetails, id=itemdetails_id)
#
#         serial_no = request.POST.get("serial_no").strip()
#         tag_no = request.POST.get("tag_no").strip()
#         room_tag = request.POST.get("room_tag").strip()
#         employee_name = request.POST.get("employee_name").strip()
#         employee_designation = request.POST.get("employee_designation").strip()
#         status = request.POST.get("status")
#         date_dispatched = request.POST.get("date_dispatched")
#
#         model_no_id = request.POST.get("model_no")
#         model_no = get_object_or_404(Items, id=model_no_id)
#
#         issued_to_id = request.POST.get("issued_to")
#         issued_to = get_object_or_404(Prosecutions, id=issued_to_id)
#
#         lpo_no_id = request.POST.get("lpo_no")
#         lpo_no = get_object_or_404(Contracts , id=lpo_no_id)
#
#         new_pdf_file = request.FILES.get('pdf_file')
#         item_details_data = {
#             'serial_no': serial_no,
#             'model_no': model_no,
#             'tag_no': tag_no,
#             'room_tag': room_tag,
#             'issued_to': issued_to,
#             'date_dispatched': date_dispatched,
#             'employee_name': employee_name,
#             'employee_designation': employee_designation,
#             'lpo_no':lpo_no,
#             'status': status,
#         }
#
#         existing_employee_name = item_details_model.employee_name
#
#         # Rename existing PDF file if the employee name has changed
#         if existing_employee_name != employee_name:
#             old_pdf_path = item_details_model.pdf_file.path
#             new_filename = f"{slugify(employee_name)}_{item_details_model.pdf_file.name.split('_')[-1]}"
#             new_path = os.path.join(os.path.dirname(old_pdf_path), new_filename)
#
#             # Rename the file
#             os.rename(old_pdf_path, new_path)
#             item_details_model.pdf_file.name = f"pdfs/itemdetails/{new_filename}"
#
#         if new_pdf_file:
#             # If a new PDF file is uploaded, delete the old PDF file if it exists
#             if item_details_model.pdf_file:
#                 default_storage.delete(item_details_model.pdf_file.name)
#             new_filename = f"{slugify(employee_name)}_{new_pdf_file.name}"
#             item_details_model.pdf_file.save(new_filename, ContentFile(new_pdf_file.read()))
#
#         # Update the ItemDetails instance with the new data
#         for key, value in item_details_data.items():
#             setattr(item_details_model, key, value)
#
#         # Save the updated ItemDetails instance
#         item_details_model.save()
#
#         item_model_id = find_item_model_id(itemdetails_id)
#         calc_total_qty()
#         calc_remaining_qty()
#
#         messages.success(request, "Item Details Edited Successfully")
#
#         return redirect('view_items_details', item_model_id)
#
#     return redirect('view_items')


def edit_item_details_save(request):
    if request.method == "POST":
        itemdetails_id = request.POST.get("detail_id")
        # Main record must exist
        item_details_model = get_object_or_404(ItemDetails, id=itemdetails_id)
        is_ajax = request.POST.get("is_ajax") == "true"

        # 1. SAFE FOREIGN KEY RETRIEVAL
        # Using .filter().first() prevents a 404 if the ID is missing or invalid
        model_no_id = request.POST.get("model_no")
        model_no = Items.objects.filter(id=model_no_id).first() if model_no_id else item_details_model.model_no

        issued_to_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.filter(
            id=issued_to_id).first() if issued_to_id else item_details_model.issued_to

        lpo_no_id = request.POST.get("lpo_no")
        lpo_no = Contracts.objects.filter(id=lpo_no_id).first() if lpo_no_id else item_details_model.lpo_no

        # 2. CAPTURE DATA
        employee_name = request.POST.get("employee_name", "").strip()

        # 3. FILE HANDLING (Only runs if a file is actually uploaded)
        new_pdf_file = request.FILES.get('pdf_file')

        # Check if name changed for existing file renaming
        if employee_name and item_details_model.employee_name != employee_name and item_details_model.pdf_file:
            try:
                old_pdf_path = item_details_model.pdf_file.path
                if os.path.exists(old_pdf_path):
                    ext = item_details_model.pdf_file.name.split('.')[-1]
                    new_filename = f"{slugify(employee_name)}_{itemdetails_id}.{ext}"
                    new_path = os.path.join(os.path.dirname(old_pdf_path), new_filename)
                    os.rename(old_pdf_path, new_path)
                    item_details_model.pdf_file.name = f"pdfs/itemdetails/{new_filename}"
            except Exception as e:
                print(f"Rename failed: {e}")

        if new_pdf_file:
            if item_details_model.pdf_file:
                default_storage.delete(item_details_model.pdf_file.name)
            new_filename = f"{slugify(employee_name)}_{new_pdf_file.name}"
            item_details_model.pdf_file.save(new_filename, ContentFile(new_pdf_file.read()), save=False)

        # 4. UPDATE CORE FIELDS
        item_details_model.serial_no = request.POST.get("serial_no", "").strip()
        item_details_model.tag_no = request.POST.get("tag_no", "").strip()
        item_details_model.room_tag = request.POST.get("room_tag", "").strip()
        item_details_model.employee_name = employee_name
        item_details_model.employee_designation = request.POST.get("employee_designation", "").strip()
        item_details_model.status = request.POST.get("status")
        item_details_model.date_dispatched = request.POST.get("date_dispatched") or None
        item_details_model.model_no = model_no
        item_details_model.issued_to = issued_to
        item_details_model.lpo_no = lpo_no

        item_details_model.save()

        # Run your calculations
        item_model_id = find_item_model_id(itemdetails_id)
        calc_total_qty()
        calc_remaining_qty()

        # 5. RESPONSE LOGIC
        # Check if the request came from AJAX (the Modal)
        if is_ajax or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Changes saved successfully!',
                'item_id': itemdetails_id  # Send this back to confirm which row to highlight
            })

        messages.success(request, "Item Details Edited Successfully")
        return redirect('view_items_details', item_model_id)

    return redirect('view_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_item_details_delete(request, id):
    itemdetails = ItemDetails.objects.get(id=id)
    item_model_id = find_item_model_id(id)
    itemdetails.delete()
    messages.success(request, "Item Details Deleted Successfully")
    calc_total_qty()
    calc_remaining_qty()
    return redirect('view_items_details',item_model_id)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_itemdetails_bulk_delete(request,id):
    if request.method == "POST":
        itemdetails_ids = request.POST.getlist('id[]')
        for id in itemdetails_ids:
            itemdetails = ItemDetails.objects.get(pk=id)
            itemdetails.delete()
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_items_details', id)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def excel_import_items_db(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.path(filename)
            itemsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
            dbframe = itemsexceldata
            for dbframe in dbframe.itertuples():
                    if Items.objects.filter(model_no = dbframe.model_no).exists():
                        messages.warning(request, dbframe.model_no + "already exists in Database")
                    else:
                        obj = Items.objects.create(model_no=dbframe.model_no, description=dbframe.description)
                        obj.save()
            filename = fs.delete(myfile.name)
            messages.success(request, "New Items uploaded to Database")
            #return render(request, 'excel_import_db.html', {'uploaded_file_url': uploaded_file_url})
            # return render(request, 'add_items.html', {})
            return redirect('view_items')
    except Exception as identifier:
        print(identifier)
    # return render(request, 'add_items.html', {})
    return redirect('view_items')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
# def excel_import_item_details_db(request):
#     global serial_number_error, column_data
#     try:
#         if request.method == 'POST' and request.FILES['myfile']:
#             myfile = request.FILES['myfile']
#             fs = FileSystemStorage()
#             filename = fs.save(myfile.name, myfile)
#             uploaded_file_url = fs.path(filename)
#             itemdetailsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
#             dbframe = itemdetailsexceldata
#             rowcount=0
#             serial_number_count=0
#             for dbframe in dbframe.itertuples():
#                 if ItemDetails.objects.filter(serial_no=dbframe.serial_no).exists():
#                     serial_number_count += 1
#                     # serial_number_error = f"{str(serial_number_count)} serial numbers already exists in Database."
#                     # messages.error(request,serial_number_error)
#                 else:
#                     obj = ItemDetails.objects.create(serial_no=str(dbframe.serial_no).strip(),
#                                                      tag_no=str(dbframe.tag_no).strip(),
#                                                      room_tag=str(dbframe.room_tag).strip(),
#                                                      status=str(dbframe.status).strip(),
#                                                      model_no=Items.objects.get(model_no=str(dbframe.model_no).strip()),
#                                                      issued_to=Prosecutions.objects.get(
#                                                          name=str(dbframe.issued_to).strip()),
#                                                      employee_name=str(dbframe.employee_name).strip(),
#                                                      employee_designation=str(dbframe.employee_designation).strip())
#
#                     rowcount += 1
#                     obj.save()
#                 serial_number_error = f"{str(serial_number_count)} serial numbers already exists in Database."
#                 new_upload_message = f"{str(rowcount)} new items uploaded to database."
#                 combined_message = f"{serial_number_error} {new_upload_message}"
#                 messages.success(request, combined_message)
#
#             fs.delete(myfile.name)
#             calc_total_qty()
#             calc_remaining_qty()
#             return redirect('view_items')
#     except Exception as identifier:
#         error = f"{str(identifier)}"
#         additional_error_message = f"{str(rowcount)} new items uploaded to database."
#         combined_error_message = f"{error}. {additional_error_message}"
#         fs.delete(myfile.name)
#         messages.error(request, combined_error_message)
#         # return redirect('view_items')
#         return redirect('add_items_details')
    # return redirect('view_items')
def excel_import_item_details_db(request):
    rowcount = 0
    serial_number_count = 0
    missing_models = set()
    missing_prosecutions = set()  # Track missing prosecutions/departments
    fs = FileSystemStorage()

    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)

        try:
            # Read CSV
            df = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')

            for row in df.itertuples():
                # --- DATA CLEANING ---
                s_no = str(row.serial_no).strip()
                if s_no.endswith('.0'):
                    s_no = s_no[:-2]

                # --- DUPLICATE CHECK ---
                if ItemDetails.objects.filter(serial_no=s_no).exists():
                    serial_number_count += 1
                    continue

                    # --- VALIDATION AND CREATION ---
                try:
                    m_no = str(row.model_no).strip()
                    i_to = str(row.issued_to).strip()

                    # These .get() calls will raise DoesNotExist if not found
                    model_obj = Items.objects.get(model_no=m_no)
                    issued_obj = Prosecutions.objects.get(name=i_to)

                    ItemDetails.objects.create(
                        serial_no=s_no,
                        tag_no=str(row.tag_no).strip(),
                        room_tag=str(row.room_tag).strip(),
                        status=str(row.status).strip(),
                        model_no=model_obj,
                        issued_to=issued_obj,
                        employee_name=str(row.employee_name).strip(),
                        employee_designation=str(row.employee_designation).strip()
                    )
                    rowcount += 1

                except Items.DoesNotExist:
                    missing_models.add(m_no)
                except Prosecutions.DoesNotExist:
                    missing_prosecutions.add(i_to)

            # --- CALCULATIONS ---
            calc_total_qty()
            calc_remaining_qty()

            # --- FINAL MESSAGES ---
            serial_info = f"{serial_number_count} serial numbers already exist."
            upload_info = f"{rowcount} new items uploaded."
            messages.success(request, f"{serial_info} {upload_info}")

            # Error message for Models
            if missing_models:
                messages.error(request, f"Items skipped: Models not found in database: {', '.join(missing_models)}")

            # Error message for Prosecutions
            if missing_prosecutions:
                messages.error(request,
                               f"Items skipped: Departments/Prosecutions not found: {', '.join(missing_prosecutions)}")

        except Exception as e:
            messages.error(request, f"Critical Error: {str(e)}")
        finally:
            if fs.exists(filename):
                fs.delete(filename)

        return redirect('view_items')

    return redirect('add_items_details')
# def search(request):
#     query = request.GET.get('q', '')
#     results = MyModel.objects.filter(name__icontains=query)
#     data = [{'id': r.id, 'text': r.name} for r in results]
#     return JsonResponse(data, safe=False)

# def upload_tags_excel(request):
#     item_model_id = request.POST.get('item_model')
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         file = request.FILES['excel_file']
#         start_tag_num = request.POST.get('start_num')
#
#
#         try:
#             # Pandas handles both .xls and .xlsx automatically
#             # header=None assumes the serials start from the very first row
#             # Check the file extension to decide the engine
#             if file.name.endswith('.xls'):
#                 df = pd.read_excel(file, header=0, engine='xlrd')
#             else:
#                 df = pd.read_excel(file, header=0, engine='openpyxl')
#
#             start_int = int(start_tag_num)
#             digit_length = len(start_tag_num)
#             updated_count = 0
#
#             # Iterate through the first column of the dataframe
#             for serial_value in df.iloc[:, 0]:
#                 serial = str(serial_value).strip()
#
#                 if not serial or serial == 'nan':  # Pandas reads empty cells as 'nan'
#                     continue
#
#                 # LOOKUP LOGIC:
#                 # Find the item where Model matches AND Serial matches
#                 # AND the Tag Number is one of your 'empty' placeholders
#                 item = ItemDetails.objects.filter(
#                     model_no_id=item_model_id,
#                     serial_no=serial
#                 ).filter(
#                     Q(tag_no__isnull=True) |
#                     Q(tag_no='') |
#                     Q(tag_no='0') |
#                     Q(tag_no='0.0') |
#                     Q(tag_no='-') |
#                     Q(tag_no='nan') |
#                     Q(tag_no='None')
#                 ).first()
#
#                 if item:
#                     current_tag_num = start_int + updated_count
#                     new_tag = f"MOJ{str(current_tag_num).zfill(digit_length)}"
#
#                     # --- NEW DUPLICATE CHECK ---
#                     # Check if this tag is already taken by ANY item in the database
#                     tag_exists = ItemDetails.objects.filter(tag_no=new_tag).exists()
#                     if tag_exists:
#                         # Option A: Skip this tag and show an error
#                         messages.error(request,
#                                        f"Conflict: Tag {new_tag} is already assigned to another item. Stopping process.")
#                         return redirect('view_items_details', item_model_id)
#
#                     item.tag_no = new_tag
#                     item.save()
#                     updated_count += 1
#
#             messages.success(request, f"Processed file. {updated_count} tags assigned.")
#
#         except Exception as e:
#             messages.error(request, f"Could not read Excel file: {e}")
#
#         return redirect('view_items_details',item_model_id)
#
#     return redirect('view_items_details', item_model_id)

def upload_tags_excel(request):
    item_model_id = request.POST.get('item_model')
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    if request.method == 'POST' and request.FILES.get('excel_file'):
        file = request.FILES['excel_file']
        start_tag_num = request.POST.get('start_num')

        try:
            # Engine selection
            engine = 'xlrd' if file.name.endswith('.xls') else 'openpyxl'
            df = pd.read_excel(file, header=0, engine=engine)

            start_int = int(start_tag_num)
            digit_length = len(start_tag_num)

            preview_list = []
            valid_count = 0
            seen_in_excel = set()  # To track duplicates within the file

            for serial_value in df.iloc[:, 0]:
                # Force clean string conversion (removes .0 from numbers)
                serial = str(serial_value).split('.')[0].strip() if '.' in str(serial_value) else str(
                    serial_value).strip()

                if not serial or serial.lower() == 'nan':
                    continue

                # 1. CHECK: Duplicate within the Excel file itself
                if serial in seen_in_excel:
                    preview_list.append({
                        'serial': serial,
                        'current_tag': "DUPLICATE IN FILE",
                        'proposed_tag': "SKIPPED",
                        'error': True,
                        'error_msg': "Serial appears twice in Excel"
                    })
                    continue
                seen_in_excel.add(serial)

                # 2. CHECK: Database lookup
                item = ItemDetails.objects.filter(
                    model_no_id=item_model_id,
                    serial_no=serial
                ).filter(
                    Q(tag_no__isnull=True) | Q(tag_no='') | Q(tag_no='0') |
                    Q(tag_no='0.0') | Q(tag_no='-') | Q(tag_no='nan') | Q(tag_no='None')
                ).first()

                if item:
                    new_tag = f"MOJ{str(start_int + valid_count).zfill(digit_length)}"

                    # 3. CHECK: Global duplicate check (Tag already in DB)
                    tag_exists = ItemDetails.objects.filter(tag_no=new_tag).exists()

                    preview_list.append({
                        'serial': serial,
                        'current_tag': item.tag_no or "Empty",
                        'proposed_tag': new_tag,
                        'error': tag_exists,
                        'error_msg': "Tag already exists in DB" if tag_exists else ""
                    })

                    if not tag_exists:
                        valid_count += 1
                else:
                    preview_list.append({
                        'serial': serial,
                        'current_tag': "NOT ELIGIBLE",
                        'proposed_tag': "SKIPPED",
                        'error': True,
                        'error_msg': "Not found or already has a valid Tag"
                    })

            return render(request, 'tags_preview.html', {
                'preview_list': preview_list,
                'item_model_id': item_model_id,
                "total": cart_total,
                "toner_stock_alert": toner_stock_alert,
                "toner_under_fifteen": toner_under_fifteen,
                'valid_count': valid_count,  # Total successful tags
                'total_rows': len(preview_list),
                'json_data': json.dumps(preview_list)
            })

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('view_items_details', item_model_id)

    return redirect('view_items_details', item_model_id)


def confirm_save_tags(request):
    item_model_id = request.POST.get('item_model_id')
    if request.method == 'POST':
        final_data = json.loads(request.POST.get('json_data'))

        updated_count = 0
        for entry in final_data:
            # Only save if there was no error and a tag was proposed
            if not entry['error'] and entry['proposed_tag'] != "SKIPPED":
                item = ItemDetails.objects.filter(
                    model_no_id=item_model_id,
                    serial_no=entry['serial']
                ).filter(
                    Q(tag_no__isnull=True) | Q(tag_no='') | Q(tag_no='0') |
                    Q(tag_no='0.0') | Q(tag_no='-') | Q(tag_no='nan') | Q(tag_no='None')
                ).first()

                if item:
                    item.tag_no = entry['proposed_tag']
                    item.save()
                    updated_count += 1

        messages.success(request, f"Successfully saved {updated_count} tags.")
        return redirect('view_items_details', item_model_id)

    return redirect('view_items_details', item_model_id)