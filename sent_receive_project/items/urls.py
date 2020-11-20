from django.urls import path
from .import views

urlpatterns=[
    path('',views.items),
    path('view_items/',views.view_items,name='view_items'),
    path('view_items_details/<int:id>',views.view_items_details,name='view_items_details'),


    path('add_items/',views.add_items,name='add_items'),
    path('add_items/add_items_save',views.add_items_save,name='add_items_save'),

    path('add_items_details/',views.add_items_details,name='add_items_details'),
    path('add_items_details/add_items_details_save',views.add_items_details_save,name='add_items_details_save'),

    path('edit_items/',views.edit_items,name='edit_items'),
    path('edit_items_form/<int:id>',views.edit_items_form,name='edit_items_form'),
    path('edit_items_form/edit_items_save',views.edit_items_save,name='edit_items_save'),
    path('edit_items_form/<int:id>',views.edit_items_form,name='edit_items_form'),
    path('edit_items_form/edit_items_delete/<int:id>',views.edit_items_delete,name='edit_items_delete')
]