from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.views import get_cart

def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        # Process the order
        order = Order(
            customer_name=request.POST['name'],
            customer_email=request.POST['email'],
            shipping_address=request.POST['address']
        )
        order.save()

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                shirt=item.shirt,
                size=item.size,
                quantity=item.quantity,
                price=item.shirt.price
            )
        
        # Clear the cart
        cart.items.all().delete()
        return redirect('checkout:order_confirmation', order_id=order.id)

    return render(request, 'checkout/checkout.html', {'cart': cart})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout/order_confirmation.html', {'order': order})