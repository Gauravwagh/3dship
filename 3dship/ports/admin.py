from django.contrib import admin

# Register your models here.
from .models import Ports, ContainerPosition, PositionConstants


class PortsAdmin(admin.ModelAdmin):
    list_display = ['port_number', 'number_of_containers']



admin.site.register(PositionConstants)
admin.site.register(Ports, PortsAdmin)
admin.site.register(ContainerPosition)
