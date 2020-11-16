from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items

def items(request):
    return HttpResponse("this is for the items page")


def view_items(request):
    return render(request,'view_items.html')


def add_items(request):
    #status=Items.objects.filter(status=Items.status)
    return render(request,'add_items.html',{"status":Items.STATUS})


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


def edit_items(request):
    return render(request,'edit_items.html')
