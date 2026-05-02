from django.shortcuts import render
from django.http import QueryDict
from products.models import Product
from main.models import HomeBanner
from .models import *

def home(request):
    home_settings = HomeBanner.objects.first()
    hero_items = HeroSlide.objects.filter(is_active=True)
    store_features = StoreFeature.objects.filter(is_active=True)
    
    # Fetch all active sections in order
    sections = ProductSection.objects.filter(is_active=True).order_by('display_order')
    
    for section in sections:
        if section.search_query:
            # Parse query params like "category=Floral&gender=men"
            qd = QueryDict(section.search_query)
            filters = {'is_active': True}
            
            if qd.get('category'): filters['category__icontains'] = qd.get('category')
            if qd.get('gender'): filters['gender'] = qd.get('gender')
            if qd.get('type'): filters['concentration'] = qd.get('type')
            if qd.get('new'): filters['is_new_arrival'] = qd.get('new').lower() == 'true'
            if qd.get('bestseller'): filters['is_bestseller'] = qd.get('bestseller').lower() == 'true'
            
            section.filtered_products = Product.objects.filter(**filters)[:section.max_products]
        else:
            section.filtered_products = section.products.filter(is_active=True)[:section.max_products]

    home_categories = HomeCategory.objects.filter(is_active=True)
    home_reviews = HomeReview.objects.filter(is_active=True)
    faq_sections = FAQSection.objects.filter(is_active=True).prefetch_related('items')

    context = {
        'home_settings': home_settings,
        'hero_items': hero_items,
        'store_features': store_features,
        'sections': sections,
        'home_categories': home_categories,
        'home_reviews': home_reviews,
        'faq_sections': faq_sections,
    }

    return render(request, 'main/home.html', context)