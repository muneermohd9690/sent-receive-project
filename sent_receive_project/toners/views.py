from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Items, Prosecutions, Toners, TonerDetails
from collections import Counter
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
import forms
from django.contrib import messages


# Create your views here.
def calc_total_qty():
    for toner in Toners.objects.annotate(tonerdetails_count=Count('tonerdetails')):
        toner.total_qty = toner.tonerdetails_count
        toner.save(update_fields=['total_qty'])


def toners(request):
    return HttpResponse("this is for the items page")


def view_toners(request):
    toners = Toners.objects.all()
    return render(request, 'view_toners.html', {"toners": toners})


def view_tonerdetails(request, id):
    tonerdetails = TonerDetails.objects.filter(toner_model=id)
    return render(request, 'view_tonerdetails.html', {"tonerdetails": tonerdetails})


def add_toners(request):
    items = Items.objects.all()
    return render(request, 'add_toners.html', {"items": items})


def add_toners_save(request):
    items = Items.objects.all()
    if request.method == "POST":
        toner_model = request.POST.get("toner_model")

        toner_printer_id = request.POST.get("toner_printer")
        toner_printer = Items.objects.get(id=toner_printer_id)

        Toners_model = Toners(toner_model=toner_model, toner_printer=toner_printer)
        Toners_model.save()
        messages.success(request, "Toner added successfully")
        calc_total_qty()
        return redirect('add_toners')
    else:
        return redirect('add_toners')


def add_tonerdetails(request):
    prosecutions = Prosecutions.objects.all()
    toners = Toners.objects.all()
    return render(request, 'add_tonerdetails.html', {"prosecutions": prosecutions, "toners": toners,
                                                     "status": TonerDetails.STATUS})


def add_tonerdetails_save(request):
    toners = Toners.objects.all()
    if request.method == "POST":
        toner_model_id = request.POST.get("toner_model")
        toner_model = Toners.objects.get(id=toner_model_id)
        name_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=name_id)
        employee_name = request.POST.get("employee_name")
        employee_designation = request.POST.get("employee_designation")
        status = request.POST.get("status")
        TonerDetails_model = TonerDetails(toner_model=toner_model, issued_to=issued_to,
                                          employee_name=employee_name, employee_designation=employee_designation,
                                          status=status)
        TonerDetails_model.save()
        messages.success(request, "Toner details added successfully")
        calc_total_qty()
        return redirect('add_tonerdetails')
    else:
        return redirect('add_tonerdetails')


def edit_toners(request):
    toners = Toners.objects.all()
    return render(request, 'edit_toners.html', {"toners": toners})


def edit_toners_form(request, id):
    items = Items.objects.all()
    toners = Toners.objects.get(id=id)
    return render(request, 'edit_toners_form.html', {"toners": toners, "items": items})


def edit_toners_save(request):
    if request.method == "POST":
        toner_id = request.POST.get("toner_id")
        toner_model = request.POST.get("toner_model")

        toner_printer_id = request.POST.get("toner_printer")
        toner_printer = Items.objects.get(id=toner_printer_id)

        # issued_to_id = request.POST.get("issued_to")
        # issued_to = Prosecutions.objects.get(id=issued_to_id)

        total_qty = request.POST.get("total_qty")
        Toners_model = Toners(id=toner_id, toner_model=toner_model, toner_printer=toner_printer, total_qty=total_qty)
        Toners_model.save()
        calc_total_qty()
        messages.success(request, "Toner updated successfully")
        return redirect('view_toners')
    else:
        return redirect('view_toners')


def edit_toners_delete(request, id):
    toners = Toners.objects.get(id=id)
    toners.delete()
    messages.success(request, "Toner deleted successfully")
    calc_total_qty()
    return redirect('edit_toners')


def edit_tonerdetails(request):
    tonerdetails = TonerDetails.objects.all()
    return render(request, 'edit_tonerdetails.html', {"tonerdetails": tonerdetails})


def edit_tonerdetails_form(request, id):
    prosecutions = Prosecutions.objects.all()
    toners = Toners.objects.all()
    tonerdetails = TonerDetails.objects.get(id=id)
    return render(request, 'edit_tonerdetails_form.html',
                  {"tonerdetails": tonerdetails, "toners": toners, "prosecutions": prosecutions,
                   "status": TonerDetails.STATUS})


def edit_tonerdetails_save(request):
    if request.method == "POST":
        tonerdetails_id = request.POST.get("tonerdetails_id")

        employee_name = request.POST.get("employee_name")
        employee_designation = request.POST.get("employee_designation")
        status = request.POST.get("status")

        # issued_to_id = request.POST.get("issued_to")
        # issued_to = Prosecutions.objects.get(id=issued_to_id)

        toner_model_id = request.POST.get("toner_model")
        toner_model = Toners.objects.get(id=toner_model_id)

        issued_to_id = request.POST.get("issued_to")
        issued_to = Prosecutions.objects.get(id=issued_to_id)

        TonerDetails_model = TonerDetails(id=tonerdetails_id, toner_model=toner_model, issued_to=issued_to,
                                          employee_name=employee_name, employee_designation=employee_designation,
                                          status=status)
        TonerDetails_model.save()
        messages.success(request, "Toner details updated successfully")
        calc_total_qty()
        return redirect('add_tonerdetails')
    else:
        return redirect('add_tonerdetails')

def edit_tonerdetails_delete(request,id):
    tonerdetails = TonerDetails.objects.get(id=id)
    tonerdetails.delete()
    messages.success(request, "Toner details deleted successfully")
    calc_total_qty()
    return redirect('edit_tonerdetails')


