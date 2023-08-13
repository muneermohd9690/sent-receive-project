from .models import Cart, Customer,CartItem
from django.contrib.contenttypes.models import ContentType

def get_total_cart_items(cart):
    cartitem = cart.cartitem_set.filter(selected=False, dispatched=False)
    total = cartitem.count()
    return total

def calc_cart_total(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
    items_in_cart = cart.cartitem_set.filter(selected=False, dispatched=False)
    # cart_total = get_total_undispatched_items(cart)
    cart_total = get_total_cart_items(cart)
    return {'cart_total':cart_total,'user_cart':cart,'items_in_cart':items_in_cart}


def get_tonerdetails_content_type_id(request):
    tonerdetails_content_type = ContentType.objects.filter(model='tonerdetails')
    for s in tonerdetails_content_type:
        tdcid = s.id # content_type_id
    return {'tdcid':tdcid}

def get_itemdetails_content_type_id(request):
    tonerdetails_content_type = ContentType.objects.filter(model='itemdetails')
    for s in tonerdetails_content_type:
        idcid = s.id # content_type_id
    return {'idcid':idcid}