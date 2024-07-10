from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.views import get_cart
from django.conf import settings
import stripe
import json
from django.http import JsonResponse

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

        # Redirect to payment page
        return redirect('checkout:payment', order_id=order.id)

    return render(request, 'checkout/checkout.html', {'cart': cart})

def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout/payment.html', {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        payment_intent_id = data.get('payment_intent_id')

        if payment_method_id:
            # Create a new PaymentIntent with a PaymentMethod ID from the client.
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Stripe expects the amount in cents
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
            )
        elif payment_intent_id:
            # Confirm the PaymentIntent to finalize the payment after handling a required action
            intent = stripe.PaymentIntent.confirm(payment_intent_id)
        
        return handle_payment_intent(intent)

    return render(request, 'checkout/order_confirmation.html', {'order': order})

def handle_payment_intent(intent):
    if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
        # Tell the client to handle the action
        return JsonResponse({
            'requires_action': True,
            'payment_intent_client_secret': intent.client_secret
        })
    elif intent.status == 'succeeded':
        # The payment didn’t need any additional actions and completed!
        # Handle post-payment fulfillment
        return JsonResponse({'success_url': redirect('checkout:order_confirmation').url})
    else:
        # Invalid status
        return JsonResponse({'error': {'message': 'Invalid PaymentIntent status'}})
