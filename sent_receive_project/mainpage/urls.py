from django.urls import path, include
from .import views

urlpatterns=[
    path('',views.mainpage,name='mainpage'),
    path('check_login/',views.check_login,name='check_login'),
    path('login/register',views.register,name='register'),
    path('logout/', views.logout_view, name='logout'),
    # path('toner_status_view/', views.toner_status_view, name='toner_status_view'),


]