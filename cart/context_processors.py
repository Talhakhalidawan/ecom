from .utils import get_cart

def cart_count(request):
    try:
        cart = get_cart(request)
        return {'cart_count': cart.total_items_count}
    except:
        return {'cart_count': 0}
