from django.urls import path
from .import views

urlpatterns=[
    path('',views.items),
    path('view_items/',views.view_items,name='view_items'),
    path('add_items/',views.add_items,name='add_items'),
    path('edit_items/',views.edit_items,name='edit_items')
]