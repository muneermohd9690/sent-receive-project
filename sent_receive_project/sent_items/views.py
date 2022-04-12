from django.shortcuts import render
from .models import SentItems

# Create your views here.
def view_sent_items(request):
    return render(request, 'view_sent_items.html')

def view_cart_items(request):
    return render(request, 'view_cart_items.html')

def add_cart_items(request):

    return render(request, 'view_cart_items.html')