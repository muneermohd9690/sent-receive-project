from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
import os
from django.conf import settings
from django.contrib.staticfiles import finders


def forms(request):
    return HttpResponse ("this is the forms page")


def sent_items_invoice(request):
    return render(request,'sent_items_invoice.html')

def issue_vouchers(request):
    return render(request,'issue_vouchers.html')


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

def print_sent_items_invoice(request):

    data = {}
    template = get_template("print_sent_items_invoice.html")
    data_p = template.render(data)
    response = BytesIO()
    #pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=links)

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")

def print_issue_vouchers(request):

    data = {}
    template = get_template("print_issue_vouchers.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")