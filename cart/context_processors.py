from .models import Cart

def cart_context(request):
    
    """
    Adds cart information to the context to be available globally.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    cart_items_count = sum(item.quantity for item in cart.items.all())
    return {
        'cart_items_count': cart_items_count,
        'cart': cart
    }
