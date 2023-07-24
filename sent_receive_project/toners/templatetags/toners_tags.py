from django import template
from django.template.defaultfilters import stringfilter

import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()

from django import template
from django.utils.html import escape

register = template.Library()

@register.filter
def replace_linebreaks(value):
    escaped_value = escape(value)
    return escaped_value.replace('\n', '<br>')
