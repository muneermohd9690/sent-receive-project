from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items, ItemDetails, Prosecutions,CartItem
from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import forms
import pandas as pd
import excel
from django.core.files.storage import FileSystemStorage
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



def calc_total_qty():
    for item in Items.objects.annotate(itemdetails_count=Count('itemdetails')):
        item.total_qty = item.itemdetails_count
        item.save(update_fields=['total_qty'])


def calc_remaining_qty():
    filters = Q(itemdetails__status="In-Stock")
    for item in Items.objects.all().annotate(itemdetails_count=Count('itemdetails', filters)):
        item.remaining_qty = item.itemdetails_count
        # TonerDetails.objects.bulk_create([TonerDetails(toner_model=toner_model) for i in range(int(quantity))])
        item.save(update_fields=['remaining_qty'])
        # Toners.objects.bulk_update(tonerdetails_count,['remaining_qty'])

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
    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    itemdetails_content_type = ContentType.objects.get(app_label='items', model='itemdetails')
    content_type_id = itemdetails_content_type.id
    joined_ids = json.dumps(joined_ids)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"itemdetails": itemdetails, "joined_ids": joined_ids, "content_type_id": content_type_id,"item_id":id,"total":cart_total,
               "toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
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
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context={"prosecutions": prosecutions, "items": items,"total":cart_total,"toner_stock_alert":toner_stock_alert,
                "toner_under_fifteen":toner_under_fifteen,"status": ItemDetails.STATUS}
    return render(request, 'add_items_details.html', context)


# this is where item details are added like modelno,serialno,department,empname
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url="login")
# def add_items_details_save(request):
#     items = Items.objects.all()
#     if request.method == "POST":
#         serial_no = request.POST.get("serial_no").strip()
#
#         model_no_id = request.POST.get("model_no").strip()
#         model_no = Items.objects.get(id=model_no_id)
#
#         tag_no = request.POST.get("tag_no").strip()
#         room_tag = request.POST.get("room_tag").strip()
#
#         name_id = request.POST.get("issued_to").strip()
#         issued_to = Prosecutions.objects.get(id=name_id)
#
#         employee_name = request.POST.get("employee_name").strip()
#
#         employee_designation = request.POST.get("employee_designation").strip()
#
#
#         status = request.POST.get("status")
#
#         ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no, tag_no=tag_no, room_tag=room_tag, issued_to=issued_to,
#                                         employee_name=employee_name, employee_designation=employee_designation,
#                                         status=status)
#         ItemDetails_model.save()
#         messages.success(request, "Item Details Added Successfully")
#         calc_total_qty()
#         calc_remaining_qty()
#         return redirect('view_items')
#     else:
#         return redirect('view_items')

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

        employee_name = request.POST.get("employee_name").strip()
        employee_designation = request.POST.get("employee_designation").strip()

        status = request.POST.get("status")

        # Save item details if serial number does not exist
        ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no, tag_no=tag_no, room_tag=room_tag,
                                        issued_to=issued_to, employee_name=employee_name,
                                        employee_designation=employee_designation, status=status)
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
def edit_item_details(request):
    itemdetails = ItemDetails.objects.all()
    items = Items.objects.all()
    prosecutions=Prosecutions.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"itemdetails": itemdetails,"toner_stock_alert":toner_stock_alert,"items": items,
               "toner_under_fifteen":toner_under_fifteen,"prosecutions":prosecutions,"status": ItemDetails.STATUS}
    return render(request, 'edit_item_details.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_item_details_form(request, id):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
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
    context = {"total": cart_total, "detail": detail, "items": items,"toner_stock_alert":toner_stock_alert,"joined_ids":joined_ids,
                        "prosecutions": prosecutions,"content_type_id":content_type_id,"toner_under_fifteen":toner_under_fifteen, "status": ItemDetails.STATUS}
    return render(request, 'edit_item_details_form.html',context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_item_details_modal(request):
    detail_id = request.GET.get('detail_id')
    items = Items.objects.all()
    prosecutions = Prosecutions.objects.all()

    # Fetch details from the database based on detail_id
    try:
        detail = ItemDetails.objects.get(pk=detail_id)
        # print(f"Model Number: {detail.model_no}, Issued to: {detail.issued_to}")
    except ItemDetails.DoesNotExist:
        print(f"ItemDetails with id={detail_id} does not exist.")

    # Render a template or return JSON data depending on your needs
    context = {'detail': detail, 'items': items, 'prosecutions': prosecutions, "status": ItemDetails.STATUS}
    return render(request, 'edit_item_details_modal.html', context)

# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url="login")
# def edit_item_details_save(request):
#     if request.method == "POST":
#         button_value = request.POST.get('save')
#         if button_value == 'save':
#             itemdetails_id = request.POST.get("detail_id")
#             serial_no = request.POST.get("serial_no").strip()
#             tag_no = request.POST.get("tag_no").strip()
#             room_tag = request.POST.get("room_tag").strip()
#             employee_name = request.POST.get("employee_name").strip()
#             employee_designation = request.POST.get("employee_designation").strip()
#             status = request.POST.get("status")
#             date_dispatched = request.POST.get("date_dispatched")
#
#             model_no_id = request.POST.get("model_no")
#             model_no = Items.objects.get(id=model_no_id)
#
#             issued_to_id = request.POST.get("issued_to")
#             issued_to = Prosecutions.objects.get(id=issued_to_id)
#
#             ItemDetails_model = ItemDetails(id=itemdetails_id, serial_no=serial_no, model_no=model_no, tag_no=tag_no,
#                                             room_tag=room_tag,issued_to=issued_to,date_dispatched=date_dispatched,
#                                             employee_name=employee_name, employee_designation=employee_designation,
#                                             status=status)
#             ItemDetails_model.save()
#             item_model_id = find_item_model_id(itemdetails_id)
#             messages.success(request, "Item Details Edited Successfully")
#             calc_total_qty()
#             calc_remaining_qty()
#             return redirect('view_items_details',item_model_id)
#         else:
#             #itemdetails_id = request.POST.get("itemdetails_id")
#             itemdetails_id = request.POST.get("detail_id")
#             serial_no = request.POST.get("serial_no").strip()
#             tag_no = request.POST.get("tag_no").strip()
#             room_tag = request.POST.get("room_tag").strip()
#             employee_name = request.POST.get("employee_name").strip()
#             employee_designation = request.POST.get("employee_designation").strip()
#             status = request.POST.get("status")
#             date_dispatched = request.POST.get("date_dispatched")
#
#             model_no_id = request.POST.get("model_no")
#             model_no = Items.objects.get(id=model_no_id)
#
#             issued_to_id = request.POST.get("issued_to")
#             issued_to = Prosecutions.objects.get(id=issued_to_id)
#
#             ItemDetails_model = ItemDetails(id=itemdetails_id, serial_no=serial_no, model_no=model_no, tag_no=tag_no,
#                                             room_tag=room_tag, issued_to=issued_to, date_dispatched=date_dispatched,
#                                             employee_name=employee_name, employee_designation=employee_designation,
#                                             status=status)
#             ItemDetails_model.save()
#             item_model_id = find_item_model_id(itemdetails_id)
#             messages.success(request, "Item Details Edited Successfully and added to dispatch")
#             calc_total_qty()
#             calc_remaining_qty()
#             return redirect('view_items_details', item_model_id)
#     else:
#         return redirect('view_items')

# @transaction.atomic
def edit_item_details_save(request):
    if request.method == "POST":
        itemdetails_id = request.POST.get("detail_id")
        serial_no = request.POST.get("serial_no").strip()
        tag_no = request.POST.get("tag_no").strip()
        room_tag = request.POST.get("room_tag").strip()
        employee_name = request.POST.get("employee_name").strip()
        employee_designation = request.POST.get("employee_designation").strip()
        status = request.POST.get("status")
        date_dispatched = request.POST.get("date_dispatched")

        model_no_id = request.POST.get("model_no")
        model_no = get_object_or_404(Items, id=model_no_id)

        issued_to_id = request.POST.get("issued_to")
        issued_to = get_object_or_404(Prosecutions, id=issued_to_id)

        item_details_data = {
            'serial_no': serial_no,
            'model_no': model_no,
            'tag_no': tag_no,
            'room_tag': room_tag,
            'issued_to': issued_to,
            'date_dispatched': date_dispatched,
            'employee_name': employee_name,
            'employee_designation': employee_designation,
            'status': status,
        }

        if request.POST.get('save') == 'save':
            # Additional logic for the 'save' case
            messages.success(request, "Item Details Edited Successfully")
        else:
            # Additional logic for the other case
            messages.success(request, "Item Details Edited Successfully and added to dispatch")

        # Common logic for both cases
        item_details_model = ItemDetails(id=itemdetails_id, **item_details_data)
        item_details_model.save()

        item_model_id = find_item_model_id(itemdetails_id)
        calc_total_qty()
        calc_remaining_qty()
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
        # data = json.loads(request.body)
        # id = data['id']
        # item_id=data['item_id']
        # print(id)
        # print(item_id)
        # for i in id:
        #     tonerdetails=TonerDetails.objects.get(pk=i)
        #     print(tonerdetails)
        #     tonerdetails.delete()
        # return JsonResponse('Item was deleted', safe=False)
        if request.method=="POST":
            itemdetails_ids=request.POST.getlist('id[]')
            for id in itemdetails_ids:
                itemdetails=ItemDetails.objects.get(pk=id)
                itemdetails.delete()
            calc_total_qty()
            calc_remaining_qty()
            return redirect('view_items_details',id)

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
def excel_import_item_details_db(request):
    global serial_number_error, column_data
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.path(filename)
            itemdetailsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
            dbframe = itemdetailsexceldata
            rowcount=0
            serial_number_count=0
            for dbframe in dbframe.itertuples():
                if ItemDetails.objects.filter(serial_no=dbframe.serial_no).exists():
                    serial_number_count += 1
                    # serial_number_error = f"{str(serial_number_count)} serial numbers already exists in Database."
                    # messages.error(request,serial_number_error)
                else:
                    obj = ItemDetails.objects.create(serial_no=str(dbframe.serial_no).strip(),
                                                     tag_no=str(dbframe.tag_no).strip(),
                                                     room_tag=str(dbframe.room_tag).strip(),
                                                     status=str(dbframe.status).strip(),
                                                     model_no=Items.objects.get(model_no=str(dbframe.model_no).strip()),
                                                     issued_to=Prosecutions.objects.get(
                                                         name=str(dbframe.issued_to).strip()),
                                                     employee_name=str(dbframe.employee_name).strip(),
                                                     employee_designation=str(dbframe.employee_designation).strip())

                    rowcount += 1
                    obj.save()
                serial_number_error = f"{str(serial_number_count)} serial numbers already exists in Database."
                new_upload_message = f"{str(rowcount)} new items uploaded to database."
                combined_message = f"{serial_number_error} {new_upload_message}"
                messages.success(request, combined_message)

            fs.delete(myfile.name)
            calc_total_qty()
            calc_remaining_qty()
            return redirect('view_items')
    except Exception as identifier:
        error = f"{str(identifier)}"
        additional_error_message = f"{str(rowcount)} new items uploaded to database."
        combined_error_message = f"{error}. {additional_error_message}"
        fs.delete(myfile.name)
        messages.error(request, combined_error_message)
        # return redirect('view_items')
        return redirect('add_items_details')
    # return redirect('view_items')

def search(request):
    query = request.GET.get('q', '')
    results = MyModel.objects.filter(name__icontains=query)
    data = [{'id': r.id, 'text': r.name} for r in results]
    return JsonResponse(data, safe=False)
