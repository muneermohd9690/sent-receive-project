from django.urls import path
from . import views

urlpatterns = [
                path('view_sent_items/', views.view_sent_items, name='view_sent_items'),
                path('view_cart_items/', views.view_cart_items, name='view_cart_items'),
                path('view_cart_items/dispatch', views.dispatch, name='dispatch'),
                path('update_items/', views.update_items, name='update_items'),
               ]
