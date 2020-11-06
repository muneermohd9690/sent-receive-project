from django.urls import path
from . import views

urlpatterns = [
    path('', views.prosecutions),
    path('view_prosecutions/', views.view_prosecutions),
    path('add_prosecutions/', views.add_prosecutions),
    path('add_prosecutions/add_prosecutions_save', views.add_prosecutions_save),
    path('edit_prosecutions/', views.edit_prosecutions)
]
