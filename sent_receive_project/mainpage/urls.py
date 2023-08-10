from django.urls import path
from .import views

urlpatterns=[
    path('',views.mainpage,name='mainpage'),
    path('check_login/',views.check_login,name='check_login'),
    path('login/register',views.register,name='register'),


]