from django.http import HttpResponse
from django.shortcuts import render

def mainpage(request):
    return render (request,'dashboard.html')


