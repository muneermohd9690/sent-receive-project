from django.urls import path
from .import views

urlpatterns=[
    path('',views.forms),
    path('sent_items_invoice/',views.sent_items_invoice,name='sent_items_invoice'),
    path('sent_items_invoice/print_sent_items_invoice',views.print_sent_items_invoice,name='print_sent_items_invoice'),
    path('issue_vouchers/',views.issue_vouchers,name='issue_vouchers'),
    path('issue_vouchers/print_issue_vouchers',views.print_issue_vouchers,name='print_issue_vouchers')

]