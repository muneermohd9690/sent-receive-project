from django.urls import path
from . import views

urlpatterns = [
    path('', views.toners),
    path('view_toners/', views.view_toners, name='view_toners'),
    path('view_tonerdetails/<int:id>', views.view_tonerdetails, name='view_tonerdetails'),

    path('add_toners/', views.add_toners, name='add_toners'),
    path('add_toners/add_toners_save', views.add_toners_save, name='add_toners_save'),

    path('add_tonerdetails/', views.add_tonerdetails, name='add_tonerdetails'),
    path('add_tonerdetails/add_tonerdetails_save', views.add_tonerdetails_save, name='add_tonerdetails_save'),

    path('edit_toners/', views.edit_toners, name='edit_toners'),
    path('edit_toners_form/<int:id>', views.edit_toners_form, name='edit_toners_form'),
    path('edit_toners_form/edit_toners_save', views.edit_toners_save, name='edit_toners_save'),
    path('edit_toners_form/edit_toners_delete/<int:id>', views.edit_toners_delete, name='edit_toners_delete'),

    path('edit_tonerdetails/', views.edit_tonerdetails, name='edit_tonerdetails'),
    path('edit_tonerdetails_form/<int:id>', views.edit_tonerdetails_form, name='edit_tonerdetails_form'),
    path('edit_tonerdetails_form/edit_tonerdetails_save', views.edit_tonerdetails_save, name='edit_tonerdetails_save'),
    path('edit_tonerdetails_form/edit_tonerdetails_delete/<int:id>', views.edit_tonerdetails_delete, name='edit_tonerdetails_delete')



]
