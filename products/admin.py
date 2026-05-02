from django.contrib import admin
from .models import Product, Size, ProductMedia, Review

# Register your models here.

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('product__name', 'user__email', 'title', 'comment')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'base_price', 'is_active')
    list_filter = ('category', 'gender', 'is_active')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes',)

admin.site.register(ProductMedia)