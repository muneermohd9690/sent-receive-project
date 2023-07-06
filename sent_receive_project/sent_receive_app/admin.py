from django.contrib import admin

from prosecutions.models import Prosecutions
from sent_items.models import Customer
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
admin.site.register(Customer)
#admin.site.register(Prosecutions, SimpleHistoryAdmin)