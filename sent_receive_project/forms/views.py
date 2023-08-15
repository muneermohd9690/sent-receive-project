import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from .models import Items,ItemDetails,Prosecutions,Toners,TonerDetails,CartItem,Cart,Forms
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.contenttypes.models import ContentType

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def forms(request):
    return HttpResponse ("this is the forms page")

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def sent_items_invoice(request):
    return render(request,'sent_items_invoice.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def issue_vouchers(request):
    return render(request,'issue_vouchers.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
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

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def print_sent_items_invoice(request,id):
    items = Cart.objects.filter(id=id)
    # cartitems=CartItem.objects.filter(cart=id)
    cartitems = CartItem.objects.filter(cart=id,dispatched=False)
    cartcount=cartitems.count()
    tdcid = get_tonerdetails_content_type_id()
    idcid = get_itemdetails_content_type_id()
    #pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=links)
    data = {'items': items,'cartitems':cartitems,'cartcount':cartcount,'tdcid':tdcid,'idcid':idcid}
    template = get_template("print_sent_items_invoice.html")
    data_p = template.render(data)
    response = BytesIO()
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def select_print_sent_items_invoice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_ids = data.get('selected_ids', [])
            id = data.get('id', '')
            cartitems = CartItem.objects.filter(id__in=selected_ids)
            cartcount = cartitems.count()
            tdcid = get_tonerdetails_content_type_id()
            idcid = get_itemdetails_content_type_id()
            data = {'cartitems': cartitems, 'cartcount': cartcount, 'tdcid': tdcid, 'idcid': idcid}
            template = get_template("print_sent_items_invoice.html")
            data_p = template.render(data)
            response = BytesIO()
            pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
            if not pdfPage.err:
                return HttpResponse(response.getvalue(), content_type="application/pdf")
            else:
                return HttpResponse("Error during PDF generation")
        except Exception as e:
            # Handle the exception gracefully but still attempt to generate PDF
            print("An error occurred during PDF generation:", str(e))
        return HttpResponse("PDF generation encountered an error")


#this is to print the issue vouchers from item details page
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
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

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
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

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
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

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
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



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def print_item_sent_invoice(request,id):
    itemdetails = ItemDetails.objects.filter(id=id)
    # for detail in itemdetails:
    #     model_id=detail.toner_model_id
    # text=find_toner_description(model_id)
    # brand=text[0]
    # device=text[1]
    data = {'itemdetails':itemdetails}
    template = get_template("print_item_sent_invoice.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

# def add_forms(request):
#     return render(request, 'add_forms.html')
#
#
# def add_forms_save(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         location = request.POST.get("location")
#         Forms_model = Forms(name=name, location=location)
#         Forms_model.save()
#         return render(request, 'add_forms.html')
#     else:
#         return render(request, 'add_forms.html')
#
#
# def view_forms(request):
#     forms = Forms.objects.all()
#     return render(request, 'view_forms.html', {"forms": forms})
#
#
# def generate_bulk_forms(request):
#     if request.method == "POST":
#         quantity= request.POST.get("quantity")
#         print(quantity)
#     else:
#         return render(request, 'add_forms.html')
#     Forms.objects.bulk_create([Forms(name=f"forms {i}",location=f"{i}")for i in range(int(quantity))])
#     return redirect('view_forms')