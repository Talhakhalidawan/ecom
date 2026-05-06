from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product, Size
from .models import Wishlist, WishlistItem
from .utils import get_wishlist

def wishlist_detail(request):
    """View to display the user's wishlist page."""
    wishlist = get_wishlist(request)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

@require_POST
def toggle_wishlist(request, product_id):
    """
    Unified toggler to add/remove products from wishlist.
    Supports both traditional forms and AJAX requests.
    """
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size')
    size = Size.objects.filter(id=size_id).first() if size_id else None
    
    wishlist = get_wishlist(request)
    existing_items = WishlistItem.objects.filter(wishlist=wishlist, product=product)
    
    if existing_items.exists():
        existing_items.delete()
        action = 'removed'
        message = f"{product.name} removed from your wishlist."
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product, size=size)
        action = 'added'
        message = f"{product.name} added to your wishlist."
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'message': message
        })
        
    messages.success(request, message)
    return redirect('wishlist:wishlist_detail')
