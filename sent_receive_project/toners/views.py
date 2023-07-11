import inspect

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Items, Prosecutions, Toners, TonerDetails,CartItem

from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
import forms
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from json import dumps
import json
from sent_items.utils import calc_cart_total
from .utils import calc_toner_stock_alert
import pandas as pd
from django.core.files.storage import FileSystemStorage
from dateutil.relativedelta import relativedelta



# Create your views here.
def calc_total_qty():
    for toner in Toners.objects.annotate(tonerdetails_count=Count('tonerdetails')):
        toner.total_qty = toner.tonerdetails_count
        toner.save(update_fields=['total_qty'])

def calc_remaining_qty():
    filters = Q(tonerdetails__status="In-Stock")
    for toner in Toners.objects.all().annotate(tonerdetails_count=Count('tonerdetails', filters)):
        toner.remaining_qty = toner.tonerdetails_count
        toner.save(update_fields=['remaining_qty'])
    #     Toners.objects.bulk_update(toner.tonerdetails_count,['remaining_qty'])


def find_toner_model_id(tonerdetails_id):
    global toner_model_id
    toner_model=TonerDetails.objects.filter(id=tonerdetails_id)
    for i in toner_model:
        toner_model_id=i.toner_model_id
    return toner_model_id

# def view_yearly_toner_estimate(request):
#     toner_counts=TonerDetails.objects.values('toner_model_id__toner_model').annotate(total_toner_count=Count('id')).filter(date_dispatched__lte=date.today(),
#                                 date_dispatched__gte=date.today() - relativedelta(days=365),status="Out-of-Stock")
#     for toner_count in toner_counts:
#         print(f"{toner_count['toner_model_id__toner_model']}: {toner_count['total_toner_count']}")
#     return HttpResponse("this is for the yearly toners report page")


def bulk_add_toner_model_id(toner_model):
    get_toner_model_id = Toners.objects.filter(toner_model=toner_model)
    for x in get_toner_model_id:
            toner_model_id = x.id
    toner_model = Toners.objects.get(id=toner_model_id)
    return toner_model


# def calc_toner_under_fifteen():
#     tonerstock=Toners.objects.filter(remaining_qty__lte=15)
#     # for toner in tonerstock:
#     #     items=Items.objects.filter(id=toner.toner_printer_id)
#     #     print(toner.toner_model,toner.toner_printer_id,toner.remaining_qty)
#     #     for item in items:
#     #         print(item.model_no, item.description)
#     return tonerstock:



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def toners(request):
    return HttpResponse("this is for the items page")


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_toners(request):
    # toners = Toners.objects.all().order_by('toner_model')
    toners = Toners.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    calc_total_qty()
    calc_remaining_qty()
    context = {"total": cart_total,"toners": toners,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'view_toners.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_tonerdetails(request, id):
    tonerdetails = TonerDetails.objects.filter(toner_model=id)
    cartitem = CartItem.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']

    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    tonerdetails_content_type = ContentType.objects.get(app_label='toners', model='tonerdetails')
    content_type_id=tonerdetails_content_type.id
    #button_state=find_button_state(tonerdetails)
    joined_ids=json.dumps(joined_ids)

    context = {"tonerdetails": tonerdetails,"joined_ids":joined_ids,"total": cart_total,"content_type_id":content_type_id,"item_id":id,
               "toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    #send_tonerdetails(request)
    return render(request, 'view_tonerdetails.html',context )


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_toners(request):
    items = Items.objects.filter(description__contains='printer')
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context={"total": cart_total,"items": items,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'add_toners.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_toners_save(request):
    items = Items.objects.all()
    if request.method == "POST":
        if request.POST['toner_model'].strip()=="":
            messages.error(request, "Toner Model is empty")
            return redirect('add_toners')
        toner_model = request.POST['toner_model'].strip()
        if Toners.objects.filter(toner_model=toner_model).exists():
            messages.error(request, "Toner Model already exists")
            return redirect('add_toners')
        elif request.POST.get('toner_model') or request.POST.get('toner_printer_id'):
             toners = Toners()
             toners.toner_model = request.POST.get("toner_model").strip()
             toner_printer_id = request.POST.get("toner_printer")
             toners.toner_printer = Items.objects.get(id=toner_printer_id)
             toners.save()
             messages.success(request,"Toner added successfully")
             return redirect('view_toners')
    else:
        return redirect('view_toners')
    # original code
    #     toner_model = request.POST.get("toner_model").strip()
    #
    #     toner_printer_id = request.POST.get("toner_printer")
    #     toner_printer = Items.objects.get(id=toner_printer_id)
    #
    #     Toners_model = Toners(toner_model=toner_model, toner_printer=toner_printer)
    #     Toners_model.save()
    #     messages.success(request, "Toner added successfully")
    #
    #     return redirect('view_toners')
    # else:
    #     return redirect('view_toners')
    # original code

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_tonerdetails(request):
    prosecutions = Prosecutions.objects.all()
    toners = Toners.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"prosecutions": prosecutions, "toners": toners,"toner_under_fifteen":toner_under_fifteen,
                                                     "status": TonerDetails.STATUS,"toner_stock_alert":toner_stock_alert}
    return render(request, 'add_tonerdetails.html',context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_tonerdetails_save(request):
    toners = Toners.objects.all()
    if request.method == "POST":
        toner_model_id = request.POST.get("toner_model")
        toner_model = Toners.objects.get(id=toner_model_id)
        name_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=name_id)
        employee_name = request.POST.get("employee_name").strip()
        employee_designation = request.POST.get("employee_designation").strip()
        status = request.POST.get("status")
        TonerDetails_model = TonerDetails(toner_model=toner_model, issued_to=issued_to,
                                          employee_name=employee_name, employee_designation=employee_designation,
                                          status=status)
        TonerDetails_model.save()
        messages.success(request, "Toner details added successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_toners')
    else:
        return redirect('view_toners')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def generate_bulk_tonerdetails(request):
    if request.method == "POST":
        quantity= request.POST.get("quantity")
        toner_model_id = request.POST.get("toner_model")
        toner_model = Toners.objects.get(id=toner_model_id)
        TonerDetails.objects.bulk_create([TonerDetails(toner_model=toner_model) for i in range(int(quantity))])
        messages.success(request, "Toner details added successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_toners')
    else:
        return redirect('view_toners')

def generate_bulk_add_toners(request):
    items = Items.objects.all()
    if request.method == "POST":
        toner_model = request.POST.get("toner_model")
        toner_printer_id = request.POST.get("toner_printer")
        toner_printer = Items.objects.get(id=toner_printer_id)
        Toners_model = Toners(toner_model=toner_model, toner_printer=toner_printer)
        Toners_model.save()

        quantity= request.POST.get("quantity")
        toner_model = bulk_add_toner_model_id(toner_model)
        TonerDetails.objects.bulk_create([TonerDetails(toner_model=toner_model) for i in range(int(quantity))])
        messages.success(request, "Toner details added successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_toners')
    else:
        return redirect('view_toners')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_toners(request):
    toners = Toners.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"toners": toners,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_toners.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_toners_form(request, id):
    items = Items.objects.all()
    toners = Toners.objects.get(id=id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"toners": toners, "items": items,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_toners_form.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_toners_save(request):
    if request.method == "POST":
        toner_id = request.POST.get("toner_id")
        toner_model = request.POST.get("toner_model").strip()

        toner_printer_id = request.POST.get("toner_printer")
        toner_printer = Items.objects.get(id=toner_printer_id)

        # issued_to_id = request.POST.get("issued_to")
        # issued_to = Prosecutions.objects.get(id=issued_to_id)

        total_qty = request.POST.get("total_qty")
        Toners_model = Toners(id=toner_id, toner_model=toner_model, toner_printer=toner_printer, total_qty=total_qty, created=datetime.now())

        Toners_model.save()
        messages.success(request,"Toner edited successfully")
        calc_total_qty()
        calc_remaining_qty()
        return redirect('view_toners')
    else:
        return redirect('edit_toners')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_toners_delete(request, id):
    toners = Toners.objects.get(id=id)
    toners.delete()
    messages.success(request, "Toner deleted successfully")
    return redirect('view_toners')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_tonerdetails(request):
    tonerdetails = TonerDetails.objects.all()
    return render(request, 'edit_tonerdetails.html', {"tonerdetails": tonerdetails})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_tonerdetails_form(request, id):
    prosecutions = Prosecutions.objects.all()
    toners = Toners.objects.all()
    #tonerdetails = TonerDetails.objects.get(id=id)
    detail = TonerDetails.objects.get(id=id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    cartitem = CartItem.objects.all()
    joined_ids = [(o.object_id, o.content_type_id) for o in cartitem]
    tonerdetails_content_type = ContentType.objects.get(app_label='toners', model='tonerdetails')
    content_type_id = tonerdetails_content_type.id
    joined_ids = json.dumps(joined_ids)
    # context = {"total": cart_total,"tonerdetails": tonerdetails, "toners": toners, "prosecutions": prosecutions,
    #                "status": TonerDetails.STATUS,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    context = {"total": cart_total, "detail": detail, "toners": toners, "prosecutions": prosecutions,"joined_ids":joined_ids,
                "status": TonerDetails.STATUS,"content_type_id":content_type_id,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_tonerdetails_form.html',context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_tonerdetails_save(request):
    caller_frame = inspect.currentframe().f_back
    caller_info = inspect.getframeinfo(caller_frame)
    caller_module = inspect.getmodule(caller_frame)
    if request.method == "POST":
        if caller_info.function != '<module>' and 'sent_items' in caller_module.__name__:
            #tonerdetails_id = request.POST.get("tonerdetails_id")
            tonerdetails_id = request.POST.get("detail_id")
            employee_name = request.POST.get("employee_name").strip()
            employee_designation = request.POST.get("employee_designation").strip()
            # date_dispatched=datetime.strptime(request.POST['date_dispatched'], '%m/%d/%Y')
            # date_dispatched = datetime.strptime(request.POST['date_dispatched'], 'YYYY-MM-DD')
            date_dispatched = request.POST.get("date_dispatched")
            status = request.POST.get("status")

            toner_model_id = request.POST.get("toner_model")
            toner_model = Toners.objects.get(id=toner_model_id)

            issued_to_id = request.POST.get("issued_to")
            issued_to = Prosecutions.objects.get(id=issued_to_id)

            TonerDetails_model = TonerDetails(id=tonerdetails_id, toner_model=toner_model, issued_to=issued_to,
                                              employee_name=employee_name, employee_designation=employee_designation,
                                              date_dispatched=date_dispatched,status=status)

            TonerDetails_model.save()
            toner_model_id=find_toner_model_id(tonerdetails_id)
            #TonerDetails_model.save(update_fields=['id','toner_model','issued_to','employee_name','employee_designation','status'])
            messages.success(request, "Toner details updated successfully and added to dispatch")
            calc_total_qty()
            calc_remaining_qty()
            return redirect('view_tonerdetails',toner_model_id)
        else:
            # tonerdetails_id = request.POST.get("tonerdetails_id")
            tonerdetails_id = request.POST.get("detail_id")
            employee_name = request.POST.get("employee_name").strip()
            employee_designation = request.POST.get("employee_designation").strip()
            # date_dispatched=datetime.strptime(request.POST['date_dispatched'], '%m/%d/%Y')
            # date_dispatched = datetime.strptime(request.POST['date_dispatched'], 'YYYY-MM-DD')
            date_dispatched = request.POST.get("date_dispatched")
            status = request.POST.get("status")

            toner_model_id = request.POST.get("toner_model")
            toner_model = Toners.objects.get(id=toner_model_id)

            issued_to_id = request.POST.get("issued_to")
            issued_to = Prosecutions.objects.get(id=issued_to_id)

            TonerDetails_model = TonerDetails(id=tonerdetails_id, toner_model=toner_model, issued_to=issued_to,
                                              employee_name=employee_name, employee_designation=employee_designation,
                                              date_dispatched=date_dispatched, status=status)

            TonerDetails_model.save()
            toner_model_id = find_toner_model_id(tonerdetails_id)
            # TonerDetails_model.save(update_fields=['id','toner_model','issued_to','employee_name','employee_designation','status'])
            messages.success(request, "Toner details updated successfully")
            calc_total_qty()
            calc_remaining_qty()
            return redirect('view_tonerdetails', toner_model_id)
        #return redirect('view_toners')
    else:
        return redirect('view_toners')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_tonerdetails_delete(request,id):
    tonerdetails = TonerDetails.objects.get(id=id)
    toner_model_id = find_toner_model_id(id)
    tonerdetails.delete()
    messages.success(request, "Toner details deleted successfully")
    calc_total_qty()
    calc_remaining_qty()
    return redirect('view_tonerdetails',toner_model_id)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_tonerdetails_bulk_delete(request,id):
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
            tonerdetails_ids=request.POST.getlist('id[]')
            for id in tonerdetails_ids:
                tonerdetails=TonerDetails.objects.get(pk=id)
                tonerdetails.delete()
            calc_total_qty()
            calc_remaining_qty()
            return redirect('view_tonerdetails',id)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def excel_import_tonerdetails_db(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.path(filename)
            tonerdetailsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
            dbframe = tonerdetailsexceldata
            for dbframe in dbframe.itertuples():
                    # if ItemDetails.objects.filter(serial_no = dbframe.serial_no).exists():
                    #     messages.warning(request, dbframe.serial_no + "already exists in Database")
                    # else:
                        obj = TonerDetails.objects.create(
                                                    toner_model=Toners.objects.get(toner_model=str(dbframe.toner_model).strip()),
                                                    issued_to=Prosecutions.objects.get(name=str(dbframe.issued_to).strip()),
                                                    employee_name=str(dbframe.employee_name).strip(),
                                                    employee_designation=str(dbframe.employee_designation).strip(),
                                                    date_dispatched=str(dbframe.date_dispatched).strip(),
                                                    status = str(dbframe.status).strip()
                                                    )
                        obj.save()
            fs.delete(myfile.name)
            calc_total_qty()
            calc_remaining_qty()
            messages.success(request, "New Items uploaded to Database")
            #return render(request, 'excel_import_db.html', {'uploaded_file_url': uploaded_file_url})
            # return render(request, 'add_items_details.html', {})
            return redirect('view_toners')
    except Exception as identifier:
        fs.delete(myfile.name)
        print(identifier)
        messages.error(request, identifier)
        # return redirect('view_items')
        return redirect('add_tonerdetails')
    # return redirect('view_items')