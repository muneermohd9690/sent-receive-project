from django.urls import path
from .import views

urlpatterns=[
    path('',views.items),
    path('view_items_quantity/',views.view_items_quantity,name='view_items_quantity'),
    path('view_items_details/<int:id>',views.view_items_details,name='view_items_details'),

    path('add_items/',views.add_items,name='add_items'),
    path('add_items_quantity/',views.add_items_quantity,name='add_items_quantity'),
    path('add_items_quantity/add_items_quantity_save',views.add_items_quantity_save,name='add_items_quantity_save'),
    path('add_items/add_items_save',views.add_items_save,name='add_items_save'),
    path('add_items_details/',views.add_items_details,name='add_items_details'),
    path('add_items_details/add_items_details_save',views.add_items_details_save,name='add_items_details_save'),

    path('edit_items/',views.edit_items,name='edit_items')
]