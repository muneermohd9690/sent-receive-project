from django.urls import path
from .import views

urlpatterns=[
                path('',views.export),
                # path('tonerdetailspdf',views.tonerdetailspdf,name='tonerdetailspdf'),
                # path('tonerdetailspdf/tonerdetails_export_topdf<int:id>',views.tonerdetails_export_topdf,name='tonerdetails_export_topdf'),
                path('itemdetails_export_topdf<int:id>',views.itemdetails_export_topdf,name='itemdetails_export_topdf'),
                path('itemdetails_export_toexcel<int:id>',views.itemdetails_export_toexcel,name='itemdetails_export_toexcel'),
                path('tonerdetails_export_topdf<int:id>',views.tonerdetails_export_topdf,name='tonerdetails_export_topdf'),
                path('tonerdetails_export_toexcel<int:id>',views.tonerdetails_export_toexcel,name='tonerdetails_export_toexcel'),
                path('sentitems_export_topdf',views.sentitems_export_topdf,name='sentitems_export_topdf'),
                path('sentitems_export_toexcel',views.sentitems_export_toexcel,name='sentitems_export_toexcel'),
]