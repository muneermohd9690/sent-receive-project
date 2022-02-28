from django.urls import path
from .import views

urlpatterns= [
    path('', views.excel),
    path('excel/excel_import_items_db/', views.excel_import_items_db, name='excel_import_items_db'),

]