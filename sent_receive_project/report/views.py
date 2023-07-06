from django.shortcuts import render
from toners.models import TonerDetails, Toners
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from django.db.models import Count, F
from datetime import datetime, date
from sent_items.utils import calc_cart_total
from toners.utils import calc_toner_stock_alert
# Create your views here.

def view_yearly_toner_estimate(request):
    toner_counts=TonerDetails.objects.values('toner_model_id__toner_model').annotate(total_toner_count=Count('id'),
        printer_model=F('toner_model_id__toner_printer_id__model_no'),printer_description=F('toner_model_id__toner_printer_id__description'))\
        .filter(date_dispatched__lte=date.today(),date_dispatched__gte=date.today() - relativedelta(days=365),status="Out-of-Stock")
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total, "toner_stock_alert": toner_stock_alert, "toner_under_fifteen": toner_under_fifteen,"toner_counts":toner_counts}
    return render(request, 'view_yearly_toner_estimate.html',context)