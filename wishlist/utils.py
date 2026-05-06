from .models import Wishlist

def get_wishlist(request):
    """Retrieves or creates a wishlist for the current user or session."""
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        wishlist, _ = Wishlist.objects.get_or_create(session_key=request.session.session_key)
    return wishlist
