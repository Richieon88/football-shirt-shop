from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from shirts.models import Shirt
from django.db.models import F


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, shirt_id):
    shirt = get_object_or_404(Shirt, id=shirt_id)
    cart = get_cart(request)
    size = request.POST.get("size")
    if size:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, shirt=shirt, size=size
        )
        if not created:
            cart_item.quantity = F("quantity") + 1
            cart_item.save()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"message": "Item added to cart"}, status=200)
    else:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Size not provided"}, status=400)
        return redirect("shirts:shirt_detail", pk=shirt_id)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    return render(
        request, "cart/cart_detail.html", {"cart": cart, "cart_items": cart_items}
    )


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=get_cart(request))
    cart_item.delete()
    return redirect("cart:cart_detail")
