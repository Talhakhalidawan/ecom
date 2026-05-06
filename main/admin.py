from django.contrib import admin
from .models import *

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)
    search_fields = ('title', 'content')

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding multiple settings instances. Singleton pattern.
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(StoreFeature)
class StoreFeatureAdmin(admin.ModelAdmin):
    list_display = ('text', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(ProductSection)
class ProductSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'card_size', 'container_width', 'display_order', 'is_active')
    list_filter = ('display_type', 'card_size', 'container_width', 'is_active')
    list_editable = ('display_type', 'display_order', 'is_active', 'card_size', 'container_width')
    search_fields = ('title',)
    filter_horizontal = ('products',)

@admin.register(HomeCategory)
class HomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'bottom_text', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(HomeReview)
class HomeReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1

@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    inlines = [FAQItemInline] # Allows editing questions directly inside the Section page


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(NavLinks)
class NavLinksAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(FooterLinks)
class FooterLinksAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'secondary_color', 'bg_color')
    list_editable = ('primary_color', 'secondary_color', 'bg_color')
    list_display_links = ('name',)

@admin.register(HomePageOrder)
class HomePageOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_order', 'section_type', 'product_section', 'is_active')
    list_editable = ('display_order', 'section_type', 'product_section', 'is_active')
    ordering = ('display_order',)