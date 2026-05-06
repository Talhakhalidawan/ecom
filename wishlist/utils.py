from .models import Wishlist

def get_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)
    return wishlist
