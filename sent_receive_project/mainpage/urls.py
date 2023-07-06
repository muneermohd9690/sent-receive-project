from django.urls import path
from .import views

urlpatterns=[
    path('',views.mainpage,name='mainpage'),
    # path('login/',views.login,name='login'),
    path('login/register',views.register,name='register'),


]