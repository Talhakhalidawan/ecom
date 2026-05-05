from django.shortcuts import render
from django.http import QueryDict
from products.models import Product
from main.models import HomeBanner
from .models import *

def home(request):
    home_settings = HomeBanner.objects.first()
    # Fetch orders
    home_orders = HomePageOrder.objects.filter(is_active=True).order_by('display_order')
    
    # Pre-fetch data for different sections
    hero_items = HeroSlide.objects.filter(is_active=True)
    store_features = StoreFeature.objects.filter(is_active=True)
    home_categories = HomeCategory.objects.filter(is_active=True)
    home_reviews = HomeReview.objects.filter(is_active=True)
    faq_sections = FAQSection.objects.filter(is_active=True).prefetch_related('items')

    # Prepare blocks with data
    blocks = []
    for order in home_orders:
        block_data = {
            'type': order.section_type,
            'order': order.display_order,
        }
        
        if order.section_type == 'products' and order.product_section:
            section = order.product_section
            if section.is_active:
                if section.search_query:
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
                block_data['section'] = section
                blocks.append(block_data)
        else:
            # For non-product blocks, we just need to ensure the data is in context
            # We'll just pass the whole blocks list and the template can access 
            # hero_items, store_features etc. directly.
            blocks.append(block_data)

    context = {
        'home_settings': home_settings,
        'hero_items': hero_items,
        'store_features': store_features,
        'home_categories': home_categories,
        'home_reviews': home_reviews,
        'faq_sections': faq_sections,
        'blocks': blocks,
    }

    return render(request, 'main/home.html', context)