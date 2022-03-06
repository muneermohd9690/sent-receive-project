from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items, ItemDetails, Prosecutions
from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
import forms
import pandas as pd
import excel
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


def calc_total_qty():
    for item in Items.objects.annotate(itemdetails_count=Count('itemdetails')):
        item.total_qty = item.itemdetails_count
        item.save(update_fields=['total_qty'])


def items(request):
    return HttpResponse("this is for the items page")


def view_items(request):
    items = Items.objects.all()
    itemdetails = ItemDetails.objects.all()
    return render(request, 'view_items.html', {"items": items})


def view_items_details(request, id):
    itemdetails = ItemDetails.objects.filter(model_no=id)
    return render(request, 'view_items_details.html', {"itemdetails": itemdetails})


def add_items(request):
    return render(request, 'add_items.html')


# this is where items are added.modelmo,description,quantity should be calculated after item_details_save
def add_items_save(request):
    if request.method == "POST":
        model_no = request.POST['model_no']
        if Items.objects.filter(model_no=model_no).exists():
            messages.error(request, "Model Number already exists")
            return redirect('add_items')
        elif request.POST.get('model_no') and request.POST.get('description'):
             items = Items()
             items.model_no = request.POST.get("model_no")
             items.description = request.POST.get("description")
             items.save()
             messages.success(request,"Item Added Successfully")
             return redirect('add_items')
    else:
        return redirect('add_items')


def add_items_details(request):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
    return render(request, 'add_items_details.html', {"prosecutions": prosecutions, "items": items,
                                                      "status": ItemDetails.STATUS})


# this is where item details are added like modelno,serialno,department,empname
def add_items_details_save(request):
    items = Items.objects.all()
    if request.method == "POST":
        serial_no = request.POST.get("serial_no")

        model_no_id = request.POST.get("model_no")
        model_no = Items.objects.get(id=model_no_id)

        tag_no = request.POST.get("tag_no")

        name_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=name_id)

        employee_name = request.POST.get("employee_name")

        employee_designation = request.POST.get("employee_designation")

        status = request.POST.get("status")

        ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no, tag_no=tag_no, issued_to=issued_to,
                                        employee_name=employee_name, employee_designation=employee_designation,
                                        status=status)
        ItemDetails_model.save()
        calc_total_qty()

        return redirect('add_items_details')
    else:
        return redirect('add_items_details')


def edit_items(request):
    items = Items.objects.all()
    return render(request, 'view_items.html', {"items": items})


def edit_items_form(request, id):
    items = Items.objects.get(id=id)
    return render(request, 'edit_items_form.html', {"items": items})


def edit_items_save(request):
    if request.method == "POST":
        items_id = request.POST.get("items_id")
        model_no = request.POST.get("model_no")
        description = request.POST.get("description")
        total_qty = request.POST.get("total_qty")
        Items_model = Items(id=items_id, model_no=model_no, description=description, total_qty=total_qty)
        Items_model.save()
        calc_total_qty()
        return redirect('view_items')
    else:
        return redirect('view_items')


def edit_items_delete(request, id):
    items = Items.objects.get(id=id)
    items.delete()
    return redirect('view_items')


def edit_item_details(request):
    itemdetails = ItemDetails.objects.all()
    return render(request, 'edit_item_details.html', {"itemdetails": itemdetails})


def edit_item_details_form(request, id):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
    itemdetails = ItemDetails.objects.get(id=id)
    return render(request, 'edit_item_details_form.html', {"itemdetails": itemdetails, "items": items,
                                                           "prosecutions": prosecutions, "status": ItemDetails.STATUS})


def edit_item_details_save(request):
    if request.method == "POST":
        itemdetails_id = request.POST.get("itemdetails_id")
        serial_no = request.POST.get("serial_no")
        tag_no = request.POST.get("tag_no")
        employee_name = request.POST.get("employee_name")
        employee_designation = request.POST.get("employee_designation")
        status = request.POST.get("status")

        model_no_id = request.POST.get("model_no")
        model_no = Items.objects.get(id=model_no_id)

        issued_to_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=issued_to_id)

        ItemDetails_model = ItemDetails(id=itemdetails_id, serial_no=serial_no, model_no=model_no, tag_no=tag_no,
                                        issued_to=issued_to,
                                        employee_name=employee_name, employee_designation=employee_designation,
                                        status=status)
        ItemDetails_model.save()
        calc_total_qty()
        return redirect('add_items_details')
    else:
        return redirect('add_items_details')


def edit_item_details_delete(request, id):
    itemdetails = ItemDetails.objects.get(id=id)
    itemdetails.delete()
    calc_total_qty()
    return redirect('edit_item_details')


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
            return render(request, 'add_items.html', {})
    except Exception as identifier:
        print(identifier)
    return render(request, 'add_items.html', {})

def excel_import_item_details_db(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.path(filename)
            itemdetailsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
            dbframe = itemdetailsexceldata
            for dbframe in dbframe.itertuples():
                    if ItemDetails.objects.filter(serial_no = dbframe.serial_no).exists():
                        messages.warning(request, dbframe.serial_no + "already exists in Database")
                    else:
                        obj = ItemDetails.objects.create(serial_no=dbframe.serial_no,tag_no=dbframe.tag_no,status=dbframe.status,
                                                    model_no=Items.objects.get(model_no=dbframe.model_no),
                                                    issued_to=Prosecutions.objects.get(name=dbframe.issued_to),
                                                    employee_name=dbframe.employee_name,employee_designation=dbframe.employee_designation)
                        obj.save()
            filename = fs.delete(myfile.name)
            calc_total_qty()
            messages.success(request, "New Items uploaded to Database")
            #return render(request, 'excel_import_db.html', {'uploaded_file_url': uploaded_file_url})
            return render(request, 'add_items_details.html', {})
    except Exception as identifier:
        print(identifier)
    return render(request, 'add_items_details.html', {})
