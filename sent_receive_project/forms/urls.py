from django.urls import path
from .import views

urlpatterns=[
    path('',views.forms),
    path('sent_items_invoice/',views.sent_items_invoice,name='sent_items_invoice'),
    path('issue_vouchers/',views.issue_vouchers,name='issue_vouchers')

]