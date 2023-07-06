from .models import Toners


def calc_toner_stock_alert(request):
    tonerstock=Toners.objects.filter(remaining_qty__lte=15)
    # for toner in Toners.objects.annotate(tonerdetails_count=Count('tonerdetails')):
    toner_stock_alert_count=tonerstock.count()
    return {"toner_stock_alert_count":toner_stock_alert_count,"tonerstock":tonerstock }
