import datetime

from django.shortcuts import render
#from .models import Items,ItemDetails,Prosecutions,Toners,TonerDetails,CartItem,Cart,Forms
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.contrib.staticfiles import finders
import os
import xlwt
from datetime import date
from django.contrib.contenttypes.models import ContentType
from items.models import Items, ItemDetails
from sent_items.models import CartItem, Cart
from toners.models import TonerDetails, Toners
import datetime
from sent_items.utils import calc_cart_total,get_tonerdetails_content_type_id,get_itemdetails_content_type_id
from operator import attrgetter
from django.db.models import F, Value, Case, When, CharField
from django.db import models

# ctid=[]
# content_type = []
# ltid = []
# liid = []

# def get_list_tonerdetailsid():
#     tonerdetails = TonerDetails.objects.all()
#     ltid = [s.id for s in tonerdetails]
#     return ltid
#
#
# def get_list_itemdetailsid():
#     itemdetails = ItemDetails.objects.all()
#     liid = [s.id for s in itemdetails]
#     return liid


# def get_tonerdetails_content_type_id():
#     tonerdetails_content_type = ContentType.objects.filter(model='tonerdetails')
#     for s in tonerdetails_content_type:
#         tdcid = s.id # content_type_id
#     return tdcid
#
# def get_itemdetails_content_type_id():
#     tonerdetails_content_type = ContentType.objects.filter(model='itemdetails')
#     for s in tonerdetails_content_type:
#         idcid = s.id # content_type_id
#     return idcid

# def get_content_type_id():
#     cartitem = CartItem.objects.all()
#     ctid = [s.content_type_id for s in cartitem]  # content_type_id
#     return ctid

#to find toner model to be defined in tonerdetails pdf export and excel export
def find_toner_model(model_id):
     global tonermodel
     toner= Toners.objects.filter(id=model_id)
     for details in toner:
         tonermodel=details.toner_model
     return tonermodel

#to find item model to be defined in itemdetails pdf export and excel export
def find_model_no(model_id):
    global itemmodel
    item = Items.objects.filter(id=model_id)
    for details in item:
        itemmodel = details.model_no
    return itemmodel
def export(request):
    return HttpResponse ("this is the export page")

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

#itemdetails pdf export
def itemdetails_export_topdf(request,id):
    itemdetails = ItemDetails.objects.filter(model_no_id=id)
    model_no=find_model_no(id)
    data = {'itemdetails':itemdetails,'model_no':model_no}
    template = get_template("itemdetailspdf_export.html")
    data_p = template.render(data)
    #response = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Item Details Report ' + str(model_no) + '.pdf'
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        #return HttpResponse(response.getvalue(), content_type="application/pdf")
        return response
    else:
        return HttpResponse("Error")

# itemdetails excel export
def itemdetails_export_toexcel(request,id):
    model_no=find_model_no(id)
    response =HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Item Details Report ' + str(model_no) + '.xls'
    wb=xlwt.Workbook(encoding='utf=8')
    ws=wb.add_sheet('Item Details Report')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Model Number','Serial Number','Tag Number','Room Tag','Issued To','Employee Name','Employee Designation','Date Dispatched','Status']
    for col_num in range (len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    rows=ItemDetails.objects.filter(model_no_id=id).values_list('model_no_id__model_no','serial_no','tag_no','room_tag','issued_to_id__name',
                                                                'employee_name','employee_designation','date_dispatched','status')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

# toneretails pdf export
def tonerdetails_export_topdf(request,id):
    tonerdetails = TonerDetails.objects.filter(toner_model_id=id)
    toner_model=find_toner_model(id)
    data = {'tonerdetails':tonerdetails,'toner_model':toner_model}
    template = get_template("tonerdetailspdf_export.html")
    data_p = template.render(data)
    #response = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=TonerReport ' + str(toner_model) + '.pdf'
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        #return HttpResponse(response.getvalue(), content_type="application/pdf")
        return response
    else:
        return HttpResponse("Error")

# toneretails excel export
def tonerdetails_export_toexcel(request,id):
    toner_model = find_toner_model(id)
    fmt = '%Y-%m-%d %H:%M:%S'
    response =HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=TonerReport ' + str(toner_model) + '.xls'
    wb=xlwt.Workbook(encoding='utf=8')
    ws=wb.add_sheet('Toner Report')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Toner Model','Issued To','Employee Name','Employee Designation','Date Dispatched','Status']
    for col_num in range (len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    rows=TonerDetails.objects.filter(toner_model_id=id).values_list('toner_model_id__toner_model','issued_to_id__name','employee_name',
                                                                    'employee_designation','date_dispatched','status')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

# sent item details pdf export
def sentitems_export_topdf(request):
    cart = Cart.objects.filter(complete=True)
    items = CartItem.objects.filter(cart_id__in=cart.values_list('id', flat=True))
    ltid = get_list_tonerdetailsid()
    liid = get_list_itemdetailsid()
    tdcid = get_tonerdetails_content_type_id()
    idcid = get_itemdetails_content_type_id()
    data = {'items':items, 'ltid': ltid, 'liid': liid,'tdcid':tdcid,'idcid':idcid}
    template = get_template("sent_itemspdf_export.html")
    data_p = template.render(data)
    #response = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Sent Item Details ' + str(date.today()) + '.pdf'
    # response['Content-Disposition'] = 'attachment; filename=TonerReport ' + '.pdf'
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return response
    else:
        return HttpResponse("Error")

    # sent item details excel export
# def sentitems_export_toexcel(request):
#         cart = Cart.objects.filter(complete=True)
#         ltid = get_list_tonerdetailsid()
#         liid = get_list_itemdetailsid()
#         tdcid = get_tonerdetails_content_type_id()
#         idcid = get_itemdetails_content_type_id()
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=Sent Item Details ' + str(date.today()) + '.xls'
#         wb = xlwt.Workbook(encoding='utf=8')
#         ws = wb.add_sheet('Toner Report')
#         row_num = 0
#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True
#         columns = ['Send Date']
#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num], font_style)
#         font_style = xlwt.XFStyle()
#         rows = CartItem.objects.filter(cart_id__in=cart.values_list('id', flat=True)).values_list('itemdetails__date_dispatched')
#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, str(row[col_num]), font_style)
#         wb.save(response)
#         return response

def sentitems_export_toexcel(request):
    if request.user.is_authenticated:
        # items = CartItem.objects.filter(dispatched=True)
        # ltid = get_list_tonerdetailsid()
        # liid = get_list_itemdetailsid()

        data_get_tonerdetails_content_type_id = get_tonerdetails_content_type_id(request)
        tdcid = data_get_tonerdetails_content_type_id['tdcid']

        data_get_itemdetails_content_type_id = get_itemdetails_content_type_id(request)
        idcid = data_get_itemdetails_content_type_id['idcid']
        # order_by_case = Case(
        #     When(content_type_id=tdcid, then='tonerdetails__date_dispatched'),
        #     When(content_type_id=idcid, then='itemdetails__date_dispatched'),
        #     default=None,
        #     output_field=models.DateTimeField()
        # )
        # Apply conditional ordering to the query
        items = (
            CartItem.objects
            .filter(dispatched=True)
            .annotate(
                date_dispatched=Case(
                    When(content_type_id=tdcid, then=F('tonerdetails__date_dispatched')),
                    When(content_type_id=idcid, then=F('itemdetails__date_dispatched')),
                    default=Value(None),
                    output_field=models.DateTimeField()
                )
            )
            .order_by('date_dispatched')
        )

    else:
        items = []


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Sent_Item_Details_{}.xls'.format(date.today())

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sent_Items')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S.No','Send Date', 'Send To', 'Product Description', 'Model No.', 'Serial No.','Received By']  # Define your column headers here
    for col_num, column_name in enumerate(columns):
        ws.write(0, col_num, column_name, font_style)

    font_style = xlwt.XFStyle()
    for row_num, item in enumerate(items, start=1):
        ws.write(row_num, 0, row_num, font_style)  # S.No
        send_date = item.content_object.date_dispatched.date()
        formatted_date = send_date.strftime('%Y-%m-%d')  # Format the date as desired, e.g., 'YYYY-MM-DD'
        ws.write(row_num, 1, formatted_date, font_style)  # Date Dispatched
        ws.write(row_num, 2, item.content_object.issued_to.name, font_style)  # Issued To

        if item.content_type.id == tdcid:
            ws.write(row_num, 3, item.content_object.toner_model.toner_printer.description + " toner",
                     font_style)  # Toner Description
            ws.write(row_num, 4, item.content_object.toner_model.toner_printer.model_no, font_style)  # Toner Model No.
            ws.write(row_num, 5, item.content_object.toner_model.toner_model, font_style)  # Toner Model
        elif item.content_type.id == idcid:
            ws.write(row_num, 3, item.content_object.model_no.description, font_style)  # Toner Description
            ws.write(row_num, 4, item.content_object.model_no.model_no, font_style)  # Toner Model No.
            ws.write(row_num, 5, item.content_object.serial_no, font_style)  # Toner Model

        ws.write(row_num, 6, item.content_object.employee_name, font_style)

    wb.save(response)
    return response
