from django.urls import path
from . import views


urlpatterns=[
    path('view_yearly_toner_estimate/',views.view_yearly_toner_estimate,name='view_yearly_toner_estimate'),

]