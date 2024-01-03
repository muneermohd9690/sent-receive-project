from django.urls import path
from . import views
#from .views import view_itemdetails_bulk_delete
import excel

urlpatterns = [
    path('', views.contracts),
    path('view_contract_details/', views.view_contract_details, name='view_contract_details'),
    path('contract_delete/<int:id>', views.contract_delete, name='contract_delete'),
    path('add_contract_details/', views.add_contract_details, name='add_contract_details'),
    path('add_contract_details/contract_details_save', views.contract_details_save, name='contract_details_save'),
    path('edit_contract_details/<int:id>', views.edit_contract_details,name='edit_contract_details'),
    path('edit_contract_details/edit_contract_details_save', views.edit_contract_details_save,
         name='edit_contract_details_save'),

]
