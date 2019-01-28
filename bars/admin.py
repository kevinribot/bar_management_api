from django.contrib import admin
from .models import Reference, Bar, Stock

# Register your models here.
admin.site.register(Reference)
admin.site.register(Bar)
admin.site.register(Stock)
