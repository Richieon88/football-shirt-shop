from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.views import get_cart
import stripe
from django.conf import settings

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    print("Checkout view called")
    cart = get_cart(request)
    print(f"Cart items: {cart.items.count()}")
    print(cart)

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

        # Create a Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(cart.total_price * 100), # Stripe expects the amount in cents
            currency='usd',
            metadata={'order_id': order.id}
        )

        # Pass the client secret to the template for Stripe.js
        return render(request, 'checkout/payment.html', {
            'client_secret': intent.client_secret,
            'order': order
        })

    return render(request, 'checkout/checkout.html', {'cart': cart})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout/order_confirmation.html', {'order': order})
