from django import template

from sent_items.models import CartItem

register =template.Library()


@register.simple_tag
def total_cartitem():
    return CartItem.objects.count()

@register.simple_tag()
def listof_cartitemids():
    return list(CartItem.objects.all().values_list('id', flat=True))
