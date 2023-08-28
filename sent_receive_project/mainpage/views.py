import pandas as pd
from django.contrib.admin import forms
from django.contrib.auth import authenticate, get_user_model, login
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
# from pandas import read_frame
import pandas

import json
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
import plotly.express as px
from django.shortcuts import render
from items.models import ItemDetails

User = get_user_model()


def check_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Add your authentication logic here.
        # For example, you can use Django's built-in authentication to check the credentials:

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # The username and password are correct.
            login(request, user)
            return JsonResponse({'is_valid': True})

        else:
            # The username and password are incorrect.
            try:
                User.objects.get(username=username)  # Check if the username exists
                return JsonResponse({'status': 'error', 'message': 'Incorrect password.'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Username does not exist.'})

    return JsonResponse({'is_valid': False})


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def mainpage(request):
    # customer, created = Customer.objects.get_or_create(user=request.user)
    # cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
    # itemsincart = cart.pk
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']

    toner_plot_html = toner_plot_view
    item_plot_html = item_plot_view
    toner_status_chart = toner_status_view(start_date,end_date)
    context = {"total": cart_total, "toner_stock_alert": toner_stock_alert, "toner_under_fifteen": toner_under_fifteen,
               "toner_plot_html": toner_plot_html, "item_plot_html": item_plot_html,"toner_status_chart":toner_status_chart}
    return render(request, 'dashboard.html', context)


def toner_plot_view():
    # Retrieve data from the model
    data = TonerDetails.objects.filter(status='Out-of-Stock')
    # Create a Pandas DataFrame to organize the data
    df = pd.DataFrame(data.values('issued_to__name'))  # Replace 'issued_to__name' with the actual field
    # Group the data by 'issued_to' and count the occurrences
    counts = df['issued_to__name'].value_counts()
    # Create the Plotly bar chart
    fig = px.bar(counts, x=counts.index, y=counts.values, title='Toners Issued to Each Prosecution')
    fig.update_xaxes(title_text='Prosecutions')
    fig.update_yaxes(title_text='Toner Count')
    # Add tooltips
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Count: %{y}')
    # Enable interactive legend
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    # Convert the figure to HTML
    toner_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return toner_plot_html


def item_plot_view():
    # Retrieve data from the model
    data = ItemDetails.objects.filter(status='Out-of-Stock')
    # Create a Pandas DataFrame to organize the data
    df = pd.DataFrame(data.values('issued_to__name'))  # Replace 'issued_to__name' with the actual field
    # Group the data by 'issued_to' and count the occurrences
    counts = df['issued_to__name'].value_counts()
    # Create the Plotly bar chart
    fig = px.bar(counts, x=counts.index, y=counts.values, title='Items Issued to Each Prosecution')
    fig.update_xaxes(title_text='Prosecutions')
    fig.update_yaxes(title_text='Item Count')
    # Add tooltips
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Count: %{y}')
    # Enable interactive legend
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    # Convert the figure to HTML
    item_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return item_plot_html

def toner_status_view(start_date=None, end_date=None):
    toner_data = TonerDetails.objects.filter(status='Out-of-Stock')
    if start_date and end_date:
        toner_data = toner_data.filter(date_dispatched__range=(start_date, end_date))

    # Create a Pandas DataFrame to organize the data
    toner_df = pd.DataFrame(toner_data.values('toner_model__toner_model'))

    # Group the data by 'status' and count the occurrences
    toner_counts = toner_df['toner_model__toner_model'].value_counts()

    # Create the Plotly bar chart
    fig = px.bar(toner_counts, x=toner_counts.index, y=toner_counts.values, title='Toner Status Distribution')
    fig.update_xaxes(title_text='Toner Model')
    fig.update_yaxes(title_text='Count')
    # Add tooltips
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Count: %{y}')
    # Enable interactive legend
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    # Convert the figure to HTML
    toner_status_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return toner_status_chart
