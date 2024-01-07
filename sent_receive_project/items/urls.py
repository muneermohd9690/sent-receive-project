from django.urls import path
from . import views
#from .views import view_itemdetails_bulk_delete
import excel

urlpatterns = [
    path('', views.items),
    path('view_items/', views.view_items, name='view_items'),
    path('view_items_details/<int:id>', views.view_items_details, name='view_items_details'),
    #path('view_items_details/edit_items_delete/<int:id>', views.edit_items_delete, name='edit_items_delete'),

    path('add_items/', views.add_items, name='add_items'),
    path('add_items/excel_import_items_db', views.excel_import_items_db, name='excel_import_items_db'),
    path('add_items/add_items_save', views.add_items_save, name='add_items_save'),

    path('add_items_details/', views.add_items_details, name='add_items_details'),
    path('add_items_details/excel_import_item_details_db', views.excel_import_item_details_db, name='excel_import_item_details_db'),
    path('add_items_details/add_items_details_save', views.add_items_details_save, name='add_items_details_save'),

    path('edit_items/', views.edit_items, name='edit_items'),
    path('edit_items_form/<int:id>', views.edit_items_form, name='edit_items_form'),
    path('edit_items_form/edit_items_save', views.edit_items_save, name='edit_items_save'),
    path('edit_items_form/edit_items_delete/<int:id>', views.edit_items_delete, name='edit_items_delete'),

    path('edit_item_details/', views.edit_item_details, name='edit_item_details'),
    path('edit_item_details/edit_item_details_save', views.edit_item_details_save, name='edit_item_details_save'),
    path('edit_item_details_form/<int:id>', views.edit_item_details_form, name='edit_item_details_form'),

    # path('edit_item_details/edit_item_details_modal/<int:id>', views.edit_item_details_modal, name='edit_item_details_modal'),
    path('edit_item_details_modal/', views.edit_item_details_modal, name='edit_item_details_modal'),
    path('edit_item_details_modal/edit_item_details_save', views.edit_item_details_save, name='edit_item_details_save'),


    path('edit_item_details_form/edit_item_details_save', views.edit_item_details_save, name='edit_item_details_save'),
    path('edit_item_details_form/edit_item_details_delete/<int:id>', views.edit_item_details_delete,
         name='edit_item_details_delete'),
    path('view_items_details/<int:id>/view_itemdetails_bulk_delete', views.view_itemdetails_bulk_delete , name='view_itemdetails_bulk_delete'),
]
