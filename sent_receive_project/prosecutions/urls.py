from django.urls import path
from . import views

urlpatterns = [
    path('', views.prosecutions),
    path('view_prosecutions/', views.view_prosecutions),
    path('add_prosecutions/', views.add_prosecutions),
    path('add_prosecutions/add_prosecutions_save', views.add_prosecutions_save),
    path('edit_prosecutions/', views.edit_prosecutions),
    path('edit_prosecutions_form/<int:prosecutions_id>', views.edit_prosecutions_form),
    path('edit_prosecutions_form/edit_prosecutions_save', views.edit_prosecutions_save),
    path('view_prosecutions/print_pdf/<int:prosecutions_id>',views.print_pdf)
]
