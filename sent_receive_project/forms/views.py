from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from .models import Items,ItemDetails,Prosecutions,Toners,TonerDetails,CartItem,Cart



def forms(request):
    return HttpResponse ("this is the forms page")


def sent_items_invoice(request):
    return render(request,'sent_items_invoice.html')

def issue_vouchers(request):
    return render(request,'issue_vouchers.html')

def test(request):
    return render(request,'test.html')

def find_description(model_id):

    description=Items.objects.filter(id=model_id)
    for desc in description:
        detail=desc.description
    text=detail.split(" ",1)
    return text

def find_toner_description(model_id):
    toner= Toners.objects.filter(id=model_id)
    for details in toner:
        printer=details.toner_printer_id
    description=Items.objects.filter(id=printer)
    for desc in description:
        detail=desc.description
        printer_model=desc.model_no
    desc_model=detail + " " +printer_model
    text=desc_model.split(" ",1)
    return text


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

def print_sent_items_invoice(request,id):
    items = Cart.objects.filter(id=id)
    cartitems=CartItem.objects.filter(cart=id)
    #pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=links)
    data = {'items': items,'cartitems':cartitems}
    template = get_template("print_sent_items_invoice.html")
    data_p = template.render(data)
    response = BytesIO()
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

#this is to print the issue vouchers from item details page
def print_issue_vouchers(request,id):
    itemdetails = ItemDetails.objects.filter(id=id)
    for detail in itemdetails:
        model_id=detail.model_no_id
    #model_id=ItemDetails.objects.get()
    text=find_description(model_id)
    brand=text[0]
    device=text[1]
    data = {'itemdetails':itemdetails,'brand':brand,'device':device}
    template = get_template("print_issue_vouchers.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")


def print_test(request):

    data = {}
    template = get_template("print_test.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

def print_toner_issue_vouchers(request,id):
    tonerdetails = TonerDetails.objects.filter(id=id)
    for detail in tonerdetails:
        model_id=detail.toner_model_id
    text=find_toner_description(model_id)
    brand=text[0]
    device=text[1]
    data = {'tonerdetails':tonerdetails,'brand':brand,'device':device}
    template = get_template("print_toner_issue_vouchers.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

def print_toner_sent_invoice(request,id):
    tonerdetails = TonerDetails.objects.filter(id=id)
    for detail in tonerdetails:
        model_id=detail.toner_model_id
    text=find_toner_description(model_id)
    brand=text[0]
    device=text[1]
    data = {'tonerdetails':tonerdetails,'brand':brand,'device':device}
    template = get_template("print_toner_sent_invoice.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

