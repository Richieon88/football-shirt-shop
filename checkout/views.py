from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.views import get_cart
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    print("Checkout view called")
    cart = get_cart(request)
    print(f"Cart items: {cart.items.count()}")
    print(cart)
    if request.method == 'POST':
        token = request.POST['stripeToken']
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

        # Create a charge: this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=int(cart.get_total_price() * 100),  # Amount in cents
                currency="usd",
                source=token,
                description="Order {}".format(order.id),
            )
        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'checkout/checkout.html', {'cart': cart, 'error': str(e)})

        # Clear the cart
        cart.items.all().delete()
        return redirect('checkout:order_confirmation', order_id=order.id)

    return render(request, 'checkout/checkout.html', {'cart': cart, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout/order_confirmation.html', {'order': order})