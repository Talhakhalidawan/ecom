from .utils import get_wishlist

def wishlist_contents(request):
    """
    Returns the IDs of products in the current user's wishlist
    """
    wishlist = get_wishlist(request)
    # Get all product IDs in the wishlist as a set for O(1) lookup
    wishlist_product_ids = set(wishlist.items.values_list('product_id', flat=True))
    
    return {
        'wishlist_product_ids': wishlist_product_ids
    }
