from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items,ItemDetails,Prosecutions



def items(request):
    return HttpResponse("this is for the items page")


def view_items_quantity(request):
    items=Items.objects.all()
    return render(request,'view_items_quantity.html',{"items":items})

def view_items_details(request,id):
    itemdetails=ItemDetails.objects.filter(model_no=id)
    return render(request,'view_items_details.html',{"itemdetails":itemdetails})




def add_items(request):
    #status=Items.objects.filter(status=Items.status)
    return render(request,'add_items.html',{"status":Items.STATUS})

def add_items_quantity(request):
    return render(request,'add_items_quantity.html')

def add_items_quantity_save(request):
    if request.method == "POST":
        model_no = request.POST.get("model_no")
        description = request.POST.get("description")
        total_qty = request.POST.get("total_qty")
        Items_model = Items(model_no=model_no,description=description,total_qty=total_qty)
        Items_model.save()
        return redirect('add_items_quantity')
    else:
        return redirect('add_items_quantity')

def add_items_save(request):
    if request.method == "POST":
        serial_no = request.POST.get("serial_no")
        model_no = request.POST.get("model_no")
        description = request.POST.get("description")
        total_qty = request.POST.get("total_qty")
        rem_qty = request.POST.get("rem_qty")
        status = request.POST.get("status")
        Items_model = Items(serial_no=serial_no, model_no=model_no,description=description,total_qty=total_qty,rem_qty=rem_qty,status=status)
        Items_model.save()
        return redirect('add_items')
    else:
        return redirect('add_items')

def add_items_details(request):
    prosecutions=Prosecutions .objects.all()
    items=Items.objects.all()
    return render(request,'add_items_details.html',{"prosecutions":prosecutions,"items":items})

def add_items_details_save(request):
    if request.method == "POST":
        serial_no = request.POST.get("serial_no")

        model_no_id = request.POST.get("model_no")
        model_no=Items.objects.get(id=model_no_id)

        name_id = request.POST.get("issued_to")
        issued_to= Prosecutions.objects.get(id=name_id)

        employee_name=request.POST.get("employee_name")
        ItemDetails_model = ItemDetails(serial_no=serial_no, model_no=model_no,issued_to=issued_to,employee_name=employee_name)
        ItemDetails_model.save()
        return redirect('add_items_details')
    else:
        return redirect('add_items_details')

def edit_items(request):
    return render(request,'edit_items.html')
