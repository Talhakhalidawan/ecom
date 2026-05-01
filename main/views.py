from django.shortcuts import render
from main.models import HomeBanner
from django.views.generic import TemplateView
from .models import *

def home(request):

    home_settings = HomeBanner.objects.first()
    hero_items = HeroSlide.objects.filter(is_active=True)
    store_features = StoreFeature.objects.filter(is_active=True)
    carousel_sections = ProductSection.objects.filter(is_active=True, display_type='carousel').prefetch_related('products')
    grid_sections = ProductSection.objects.filter(is_active=True, display_type='grid').prefetch_related('products')
    home_categories = HomeCategory.objects.filter(is_active=True)
    home_reviews = HomeReview.objects.filter(is_active=True)
    faq_sections = FAQSection.objects.filter(is_active=True).prefetch_related('items')

    context = {
        'home_settings': home_settings,
        'hero_items': hero_items,
        'store_features': store_features,
        'carousel_sections': carousel_sections,
        'grid_sections': grid_sections,
        'home_categories': home_categories,
        'home_reviews': home_reviews,
        'faq_sections': faq_sections,
    }

    return render(request, 'main/home.html', context)