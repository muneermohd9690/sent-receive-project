from django.urls import path
from .import views

urlpatterns= [
    path('', views.excel),
    path('excel_import_db/', views.excel_import_db, name='excel_import_db')

]