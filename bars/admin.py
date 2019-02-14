from django.contrib import admin
from .models import Reference, Bar, Stock, Order, OrderItem
from django.core import serializers
from django.http import HttpResponse


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

	
admin.site.add_action(export_as_json, 'export_selected')


# Reference
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['ref', 'name', 'description']
    ordering = ['ref']

admin.site.register(Reference, ReferenceAdmin)


# Bar
class BarAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    ordering = ['pk']

admin.site.register(Bar, BarAdmin)


# Stock
class StockAdmin(admin.ModelAdmin):
    list_display = ['bar', 'reference', 'stock']
    ordering = ['bar', '-stock']

admin.site.register(Stock, StockAdmin)


# Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'bar', 'created']
    ordering = ['created']

admin.site.register(Order, OrderAdmin)


# OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'reference']
    ordering = ['order']

admin.site.register(OrderItem, OrderItemAdmin)

