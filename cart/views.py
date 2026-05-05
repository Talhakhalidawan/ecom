from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product, Size
from .models import Cart, CartItem
from .utils import get_cart

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

from django.http import JsonResponse

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size_id = request.POST.get('size')
    
    size = None
    if size_id:
        size = get_object_or_404(Size, id=size_id)
    
    cart = get_cart(request)
    
    # Check if item with same size already exists
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        defaults={'quantity': 0}
    )
    
    new_quantity = cart_item.quantity + quantity
    if new_quantity > product.stock_quantity:
        new_quantity = product.stock_quantity
    
    cart_item.quantity = new_quantity
    cart_item.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} has been added to your collection.",
            'cart_count': cart.total_items_count
        })

    messages.success(request, f"{product.name} has been added to your collection.")
    return redirect('cart:cart_detail')

@require_POST
def update_cart(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get('action')
    
    if action == 'increment':
        if cart_item.quantity < cart_item.product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Maximum stock reached.',
                    'is_max': True
                })
            messages.warning(request, "Maximum stock reached for this item.")
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'action': 'removed',
                    'cart_count': cart.total_items_count,
                    'cart_total': cart.total_price
                })
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity,
            'line_total': cart_item.line_total,
            'cart_total': cart.total_price,
            'cart_count': cart.total_items_count,
            'is_min': cart_item.quantity <= 1,
            'is_max': cart_item.quantity >= cart_item.product.stock_quantity
        })

    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_items_count,
            'cart_total': cart.total_price
        })

    messages.info(request, "Item removed from your collection.")
    return redirect('cart:cart_detail')
