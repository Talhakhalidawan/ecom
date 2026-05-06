from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product, Size
from .models import Wishlist, WishlistItem
from .utils import get_wishlist

def wishlist_detail(request):
    wishlist = get_wishlist(request)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size')
    size = None
    if size_id:
        size = get_object_or_404(Size, id=size_id)
    
    wishlist = get_wishlist(request)
    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product,
        size=size
    )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} added to your wishlist.",
            'is_new': created
        })
    
    if created:
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
        
    return redirect('wishlist:wishlist_detail')

@require_POST
def remove_from_wishlist(request, item_id):
    wishlist = get_wishlist(request)
    item = get_object_or_404(WishlistItem, id=item_id, wishlist=wishlist)
    item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': "Item removed from your wishlist."
        })
        
    messages.info(request, "Item removed from your wishlist.")
    return redirect('wishlist:wishlist_detail')
