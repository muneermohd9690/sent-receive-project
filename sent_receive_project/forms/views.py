from django.http import HttpResponse
from django.shortcuts import render

def forms(request):
    return HttpResponse ("this is the forms page")


def sent_items_invoice(request):
    return render(request,'sent_items_invoice.html')

def issue_vouchers(request):
    return render(request,'issue_vouchers.html')

def prosecution_printouts(request):
    return render(request,'prosecution_printouts.html')