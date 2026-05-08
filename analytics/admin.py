from django.contrib import admin
from .models import PageVisit, ProductEvent

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'session_key', 'created_at', 'ip_address')
    list_filter = ('created_at', 'path')
    search_fields = ('path', 'session_key', 'ip_address')
    readonly_fields = ('created_at',)

@admin.register(ProductEvent)
class ProductEventAdmin(admin.ModelAdmin):
    list_display = ('product', 'event_type', 'user', 'created_at', 'session_key')
    list_filter = ('event_type', 'created_at', 'product')
    search_fields = ('product__name', 'session_key')
    readonly_fields = ('created_at',)
