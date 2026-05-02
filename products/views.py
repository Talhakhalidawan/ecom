from django.shortcuts import render, get_object_or_identity, get_object_or_404
from .models import Product, Size
from django.db.models import Q

def search_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    gender = request.GET.get('gender', '')
    size_ids = request.GET.getlist('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'new')

    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        )

    if category:
        products = products.filter(category__icontains=category)
    
    if gender:
        products = products.filter(gender=gender)
    
    if size_ids:
        products = products.filter(sizes__id__in=size_ids).distinct()
    
    if min_price:
        try:
            products = products.filter(base_price__gte=float(min_price))
        except: pass
    
    if max_price:
        try:
            products = products.filter(base_price__lte=float(max_price))
        except: pass

    # Sorting
    if sort == 'price_low':
        products = products.order_by('base_price')
    elif sort == 'price_high':
        products = products.order_by('-base_price')
    else:
        products = products.order_by('-created_at')

    # Get filter options
    all_sizes = Size.objects.all()
    # Get unique categories from existing products to be dynamic
    all_categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'query': query,
        'all_sizes': all_sizes,
        'all_categories': all_categories,
        'current_category': category,
        'current_gender': gender,
        'current_sizes': [int(s) for s in size_ids if s.isdigit()],
        'current_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'products/search.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {'product': product}
    return render(request, 'products/details.html', context)
