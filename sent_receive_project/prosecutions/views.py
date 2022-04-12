from io import BytesIO

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from xhtml2pdf import pisa
from .models import Prosecutions
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


def prosecutions(request):
    return HttpResponse("this for prosecutions")


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_prosecutions(request):
    prosecutions = Prosecutions.objects.all()
    return render(request, 'view_prosecutions.html', {"prosecutions": prosecutions})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_prosecutions(request):
    return render(request, 'add_prosecutions.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_prosecutions_save(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        Prosecutions_model = Prosecutions(name=name, location=location)
        Prosecutions_model.save()
        return render(request, 'add_prosecutions.html')
    else:
        return render(request, 'add_prosecutions.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions(request):
    prosecutions = Prosecutions.objects.all()
    return render(request, 'edit_prosecutions.html', {"prosecutions": prosecutions})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_form(request, prosecutions_id):
    prosecutions = Prosecutions.objects.get(id=prosecutions_id)
    return render(request, 'edit_prosecutions_form.html', {"prosecutions": prosecutions})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_save(request):
    if request.method == "POST":
        prosecutions_id = request.POST.get("prosecutions_id")
        name = request.POST.get("name")
        location = request.POST.get("location")
        Prosecutions_model = Prosecutions(id=prosecutions_id, name=name, location=location)
        Prosecutions_model.save()
        return view_prosecutions(request)
    else:
        return view_prosecutions(request)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_delete(request, prosecutions_id):
    prosecutions = Prosecutions.objects.get(id=prosecutions_id)
    prosecutions.delete()
    return edit_prosecutions(request)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def print_pdf(request, prosecutions_name):
    prosecutions = Prosecutions.objects.get(name=prosecutions_name)
    data = {'prosecutions': prosecutions}
    template = get_template("pdf_prosecutions.html")
    data_p = template.render(data)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error")
