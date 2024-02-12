import pandas as pd
from django.contrib.admin import forms
from django.contrib.auth import authenticate, get_user_model, login,logout
from django.db import IntegrityError, transaction
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
from django.contrib.auth.views import LogoutView
import json
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
import plotly.express as px
from django.shortcuts import render
from items.models import ItemDetails
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


def check_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use case-insensitive lookup for username (default behavior)
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Username does not exist.'})

        # Add your authentication logic here.
        # For example, you can use Django's built-in authentication to check the credentials:
        authenticated_user = authenticate(request, username=user.username, password=password)

        if authenticated_user is not None:
            # The username and password are correct.
            login(request, authenticated_user)
            return JsonResponse({'is_valid': True})
        else:
            # The username and password are incorrect.
            return JsonResponse({'status': 'error', 'message': 'Incorrect password.'})

    return JsonResponse({'is_valid': False})


# def register(request):
#     form = CreateUserForm()
#
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, 'Account was created for ' + user)
#             return redirect('login')
#         else:
#             # Return form errors as JSON
#             errors = {field: form.errors[field][0] for field in form.errors}
#
#     context = {'form': form}
#     return render(request, 'register.html', context)
#


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print(f"Valid Form Data: {form.cleaned_data}")
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                messages.success(request, 'Account was created for ' + user.username)
                return redirect('login')
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                messages.error(request, 'IntegrityError occurred. See console for details.')
        else:
            # Return form errors as JSON
            errors = {field: form.errors[field][0] for field in form.errors}
            # return JsonResponse({'success': False, 'message': 'Form validation failed.', 'errors': errors})

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
    toner_status_data = toner_status_view(start_date, end_date)
    # toner_status_chart = toner_status_view(start_date,end_date)
    toner_status_chart=toner_status_data['toner_status_chart']
    has_data = toner_status_data['has_data']

    context = {"total": cart_total, "toner_stock_alert": toner_stock_alert, "toner_under_fifteen": toner_under_fifteen,
               "toner_plot_html": toner_plot_html, "item_plot_html": item_plot_html,"toner_status_chart":toner_status_chart,"has_data": has_data}
    # return render(request, 'dashboard.html', context)
    # return render(request, 'mainpage.html', context)
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

# def toner_status_view(start_date=None, end_date=None):
#     toner_data = TonerDetails.objects.filter(status='Out-of-Stock')
#     if start_date and end_date:
#         toner_data = toner_data.filter(date_dispatched__range=(start_date, end_date))
#
#     has_data = toner_data.exists()
#     # Create a Pandas DataFrame to organize the data
#     toner_df = pd.DataFrame(toner_data.values('toner_model__toner_model'))
#
#     # Group the data by 'status' and count the occurrences
#     toner_counts = toner_df['toner_model__toner_model'].value_counts()
#
#     # Create the Plotly bar chart
#     fig = px.bar(toner_counts, x=toner_counts.index, y=toner_counts.values, title='Toner Status Distribution')
#     fig.update_xaxes(title_text='Toner Model')
#     fig.update_yaxes(title_text='Count')
#     # Add tooltips
#     fig.update_traces(hovertemplate='<b>%{x}</b><br>Count: %{y}')
#     # Enable interactive legend
#     fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
#     # Convert the figure to HTML
#     toner_status_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')
#     # return toner_status_chart
#     return {'toner_status_chart': toner_status_chart, 'has_data': has_data}

def toner_status_view(start_date=None, end_date=None):
    # Filter the data based on the selected date range
    toner_data = TonerDetails.objects.filter(status='Out-of-Stock')
    if start_date and end_date:
        toner_data = toner_data.filter(date_dispatched__range=(start_date, end_date))

    # Check if there is any data available
    has_data = toner_data.exists()

    if has_data:
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
    else:
        # If there's no data, set toner_status_chart to an empty string
        toner_status_chart = ''

    # Return both the chart and the has_data flag
    return {'toner_status_chart': toner_status_chart, 'has_data': has_data}

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect_url': '/login/'})