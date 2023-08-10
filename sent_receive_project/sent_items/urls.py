from django.urls import path
from . import views

urlpatterns = [
                path('view_sent_items/', views.view_sent_items, name='view_sent_items'),
                path('dispatch/', views.dispatch, name='dispatch'),

                path('view_cart_items/', views.view_cart_items, name='view_cart_items'),
                path('update_items/', views.update_items, name='update_items'),
                path('bulk_update_items/', views.bulk_update_items, name='bulk_update_items'),
                path('view_cart_items/remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
               ]
