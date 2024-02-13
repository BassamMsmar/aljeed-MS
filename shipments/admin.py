from django.contrib import admin
from .models import Shipment
# from drivers.models import Driver

# Register your models here.
# class DriverTabular(admin.TabularInline):
#     model = Driver


class ShipmentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'driver', 'customer_branch', 'destination', 'status']
    list_filter = ['user', 'driver', 'customer_branch', 'destination', 'status']
    search_fields = ['user', 'driver', 'customer_branch', 'destination', 'status']
    # inlines = [DriverTabular]
               
admin.site.register(Shipment, ShipmentsAdmin)