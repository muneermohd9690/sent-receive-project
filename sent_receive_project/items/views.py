from django.http import HttpResponse
from django.shortcuts import render

def items(request):
    return HttpResponse("this is for the items page")


def view_items(request):
    return render(request,'view_items.html')


def add_items(request):
    return render(request,'add_items.html')


def edit_items(request):
    return render(request,'edit_items.html')
