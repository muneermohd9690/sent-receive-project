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




def get_list_tonerdetailsid():
    tonerdetails = TonerDetails.objects.all()
    ltid = [s.id for s in tonerdetails]
    return ltid


def get_list_itemdetailsid():
    itemdetails = ItemDetails.objects.all()
    liid = [s.id for s in itemdetails]
    return liid


def get_tonerdetails_content_type_id():
    tonerdetails_content_type = ContentType.objects.filter(model='tonerdetails')
    for s in tonerdetails_content_type:
        tdcid = s.id # content_type_id
    return tdcid

def get_itemdetails_content_type_id():
    tonerdetails_content_type = ContentType.objects.filter(model='itemdetails')
    for s in tonerdetails_content_type:
        idcid = s.id # content_type_id
    return idcid

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
def sentitems_export_toexcel(request):
        cart = Cart.objects.filter(complete=True)
        ltid = get_list_tonerdetailsid()
        liid = get_list_itemdetailsid()
        tdcid = get_tonerdetails_content_type_id()
        idcid = get_itemdetails_content_type_id()
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Sent Item Details ' + str(date.today()) + '.xls'
        wb = xlwt.Workbook(encoding='utf=8')
        ws = wb.add_sheet('Toner Report')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Send Date']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = CartItem.objects.filter(cart_id__in=cart.values_list('id', flat=True)).values_list('itemdetails__date_dispatched')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response


