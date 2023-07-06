import pandas as pd
from django.contrib.admin import forms
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from .models import CreateUserForm
from django.contrib import messages
# from sent_items.views import get_total_cart_items
# from sent_items.models import SentItems, Cart, CartItem,Customer
from sent_items.utils import calc_cart_total
from toners.utils import calc_toner_stock_alert
from toners.models import TonerDetails
from prosecutions.models import Prosecutions
#from pandas import read_frame
import pandas
import plotly
import plotly.express as px
import json
from django.db.models import Count


# def login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return render(request, 'dashboard.html')
#         else:
#             messages.info(request,'Username or password is incorrect')
#             return redirect('login')
#     context = {}
#     return render(request, 'dashboard.html',context)
def register(request):
    form=CreateUserForm()

    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')

    context={'form':form}
    return render(request,'register.html',context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def mainpage(request):
    # customer, created = Customer.objects.get_or_create(user=request.user)
    # cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
    # itemsincart = cart.pk
    data_calc_cart_total = calc_cart_total(request)
    cart_total=data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

    # return render(request,'dashboard.html',context)
    # tonerdetails=TonerDetails.objects.all()
    # for detail in tonerdetails:
    #     print(Count(detail.toner_model.toner_model))



    context = {"total": cart_total, "toner_stock_alert": toner_stock_alert, "toner_under_fifteen": toner_under_fifteen}
    return render(request, 'dashboard.html',context)


