from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Prosecutions


def prosecutions(request):
    return HttpResponse("this for prosecutions")


def view_prosecutions(request):
    return render(request, 'view_prosecutions.html')


def add_prosecutions(request):
    return render(request, 'add_prosecutions.html')


def add_prosecutions_save(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        Prosecutions_model = Prosecutions(name=name, location=location)
        Prosecutions_model.save()
        return render(request, 'add_prosecutions.html')
    else:
        return render(request, 'add_prosecutions.html')


def edit_prosecutions(request):
    return render(request, 'edit_prosecutions.html')
