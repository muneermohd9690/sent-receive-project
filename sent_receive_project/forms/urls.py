from django.urls import path
from .import views

urlpatterns=[
    path('',views.forms),
    path('sent_items_invoice/',views.sent_items_invoice,name='sent_items_invoice'),
    path('sent_items_invoice/print_sent_items_invoice<int:id>',views.print_sent_items_invoice,name='print_sent_items_invoice'),
    path('sent_items_invoice/print_toner_sent_invoice<int:id>',views.print_toner_sent_invoice,name='print_toner_sent_invoice'),


    path('issue_vouchers/',views.issue_vouchers,name='issue_vouchers'),
    path('issue_vouchers/print_issue_vouchers/<int:id>',views.print_issue_vouchers,name='print_issue_vouchers'),
    path('issue_vouchers/print_toner_issue_vouchers/<int:id>',views.print_toner_issue_vouchers,name='print_toner_issue_vouchers'),


    path('test/',views.test,name='test'),
    path('test/print_test',views.print_test,name='print_test')

]