from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'base_price', 'is_active')
    list_filter = ('category', 'gender', 'is_active')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes',)

admin.site.register(ProductMedia)
admin.site.register(Review)