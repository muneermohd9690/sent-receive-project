from django.urls import path
from . import views

urlpatterns = [
    path('', views.prosecutions),
    path('view_prosecutions/', views.view_prosecutions, name='view_prosecutions'),
    path('view_prosecutions/print_pdf/<int:id>',views.print_pdf,name='print_pdf'),

    path('add_prosecutions/', views.add_prosecutions,name='add_prosecutions'),
    path('add_prosecutions/add_prosecutions_save', views.add_prosecutions_save,name='add_prosecutions_save'),

    path('edit_prosecutions/', views.edit_prosecutions,name='edit_prosecutions'),
    path('edit_prosecutions_form/<int:prosecutions_id>', views.edit_prosecutions_form,name='edit_prosecutions_form'),
    path('edit_prosecutions_form/edit_prosecutions_save', views.edit_prosecutions_save,name='edit_prosecutions_save'),
    path('edit_prosecutions_form/edit_prosecutions_delete/<int:prosecutions_id>',views.edit_prosecutions_delete,name='edit_prosecutions_delete')


]
