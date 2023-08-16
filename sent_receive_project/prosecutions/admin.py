
from django.contrib import admin
from .models import Prosecutions


class ProsecutionsAdmin(admin.ModelAdmin):
    prosecutions_display = ('id', 'name')


admin.site.register(Prosecutions, ProsecutionsAdmin)

