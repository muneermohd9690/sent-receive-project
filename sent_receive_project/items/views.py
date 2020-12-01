from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items,ItemDetails,Prosecutions
from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q


def calc_total_qty():
    for item in Items.objects.annotate(itemdetails_count=Count('itemdetails')):
        item.total_qty = item.itemdetails_count
        item.save(update_fields=['total_qty'])


def items(request):
    return HttpResponse("this is for the items page")


def view_items(request):
    items=Items.objects.all()
    itemdetails=ItemDetails.objects.all()
    return render(request,'view_items.html',{"items":items})

def view_items_details(request,id):
    itemdetails=ItemDetails.objects.filter(model_no=id)
    return render(request,'view_items_details.html',{"itemdetails":itemdetails})



def add_items(request):
    return render(request,'add_items.html')

#this is where items are added.modelmo,description,quantity should be calculated after item_details_save
def add_items_save(request):
    if request.method == "POST":
        model_no = request.POST.get("model_no")
        description = request.POST.get("description")
        #total_qty = request.POST.get("total_qty"),total_qty=total_qty
        Items_model = Items(model_no=model_no,description=description)
        Items_model.save()
        return redirect('add_items')
    else:
        return redirect('add_items')



def add_items_details(request):
    prosecutions=Prosecutions .objects.all()
    items=Items.objects.all()
    return render(request,'add_items_details.html',{"prosecutions":prosecutions,"items":items})

#this is where item details are added like modelno,serialno,department,empname
def add_items_details_save(request):
    items=Items.objects.all()
    if request.method == "POST":
        serial_no = request.POST.get("serial_no")

        model_no_id = request.POST.get("model_no")
        model_no=Items.objects.get(id=model_no_id)

        name_id = request.POST.get("issued_to")
        issued_to= Prosecutions.objects.get(id=name_id)

        employee_name=request.POST.get("employee_name")
        ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no,issued_to=issued_to,employee_name=employee_name)
        ItemDetails_model.save()
        calc_total_qty()

        return redirect('add_items_details')
    else:
        return redirect('add_items_details')

def edit_items(request):
    items = Items.objects.all()
    return render(request, 'edit_items.html', {"items": items})

def edit_items_form(request,id):
    items=Items.objects.get(id=id)
    return render(request, 'edit_items_form.html', {"items":items})


def edit_items_save(request):
    if request.method == "POST":
        items_id = request.POST.get("items_id")
        model_no = request.POST.get("model_no")
        description = request.POST.get("description")
        total_qty = request.POST.get("total_qty")
        Items_model = Items(id=items_id, model_no=model_no, description=description,total_qty=total_qty)
        Items_model.save()
        return redirect('edit_items')
    else:
        return redirect('edit_items')

def edit_items_delete(request,id):
    items = Items.objects.get(id=id)
    items.delete()
    return redirect('edit_items')

def edit_item_details(request):
    itemdetails=ItemDetails.objects.all()
    return render(request,'edit_item_details.html',{"itemdetails":itemdetails})

def edit_item_details_form(request,id):
    prosecutions = Prosecutions.objects.all()
    items = Items.objects.all()
    itemdetails = ItemDetails.objects.get(id=id)
    return render(request,'edit_item_details_form.html',{"itemdetails": itemdetails,"items":items,"prosecutions":prosecutions})


def edit_item_details_save(request):
    if request.method == "POST":
        itemdetails_id = request.POST.get("itemdetails_id")
        serial_no = request.POST.get("serial_no")
        employee_name = request.POST.get("employee_name")

        model_no_id = request.POST.get("model_no")
        model_no=Items.objects.get(id=model_no_id)

        issued_to_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=issued_to_id)

        ItemDetails_model = ItemDetails(id= itemdetails_id ,serial_no=serial_no, model_no=model_no, issued_to=issued_to,
                                        employee_name=employee_name)
        ItemDetails_model.save()
        return redirect('add_items_details')
    else:
        return redirect('add_items_details')

def edit_item_details_delete(request,id):
    itemdetails = ItemDetails.objects.get(id=id)
    itemdetails.delete()
    calc_total_qty()
    return redirect('edit_item_details')