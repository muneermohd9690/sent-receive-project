from io import BytesIO

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from xhtml2pdf import pisa
from .models import Prosecutions
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from sent_items.utils import calc_cart_total
from toners.utils import calc_toner_stock_alert
from django.contrib import messages



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def prosecutions(request):
    return HttpResponse("this for prosecutions")


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_prosecutions(request):
    prosecutions = Prosecutions.objects.all().order_by('location')
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"prosecutions": prosecutions,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'view_prosecutions.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_prosecutions(request):
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'add_prosecutions.html',context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_prosecutions_save(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        location = request.POST.get("location").strip()
        Prosecutions_model = Prosecutions(name=name, location=location)
        Prosecutions_model.save()
        messages.success(request, "Prosecution added successfully")
        return redirect('view_prosecutions')
    else:
        return redirect('view_prosecutions')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions(request):
    prosecutions = Prosecutions.objects.all()
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"prosecutions": prosecutions,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_prosecutions.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_form(request, prosecutions_id):
    prosecutions = Prosecutions.objects.get(id=prosecutions_id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total, "prosecutions": prosecutions,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    return render(request, 'edit_prosecutions_form.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_save(request):
    if request.method == "POST":
        prosecutions_id = request.POST.get("prosecutions_id")
        name = request.POST.get("name").strip()
        location = request.POST.get("location").strip()
        Prosecutions_model = Prosecutions(id=prosecutions_id, name=name, location=location)

        #Prosecutions_model._change_reason = 'edited the prosecution'
        Prosecutions_model.save()

        messages.success(request, "Prosecution edited successfully")
        return redirect('view_prosecutions')
    else:
        return redirect('view_prosecutions')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_prosecutions_delete(request, prosecutions_id):
    prosecutions = Prosecutions.objects.get(id=prosecutions_id)
    prosecutions.delete()
    messages.success(request, "Prosecution deleted successfully")
    return redirect('view_prosecutions')


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
