from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order, OrderItem
from cart.models import Cart
import stripe
import json
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

# Retrieve or create a cart for the user
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

# Send order confirmation email
def send_order_confirmation_email(order):
    subject = "Order Confirmation - My Soccer Shirts"
    # Prepare the HTML and plain-text message
    html_message = render_to_string('checkout/order_confirmation_email.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.customer_email]

    # Send the email
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

# Checkout view to handle order creation and redirection to payment
def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        # Create the order
        order = Order(
            customer_name=request.POST['name'],
            customer_email=request.POST['email'],
            shipping_address=request.POST['address'],
        )
        order.save()

        # Create OrderItems from CartItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                shirt=item.shirt,
                size=item.size,
                quantity=item.quantity,
                price=item.shirt.price,
            )

        # Clear the cart after transferring items
        cart.items.all().delete()

        # Send the order confirmation email
        send_order_confirmation_email(order)

        # Redirect to payment page with order id
        return redirect('checkout:payment', order_id=order.id)

    return render(request, 'checkout/checkout.html', {'cart': cart})

# Payment view to render payment page and handle Stripe public key
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout/payment.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

# Order confirmation view to handle Stripe PaymentIntent and confirmation response
def order_confirmation(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        
        if request.method == 'POST':
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')
            payment_intent_id = data.get('payment_intent_id')

            # Ensure amount is in cents for Stripe
            amount = int(order.total_price * 100)

            if payment_method_id:
                # Create PaymentIntent
                intent = stripe.PaymentIntent.create(
                    amount=amount,  # Stripe amount in cents
                    currency='usd',
                    payment_method=payment_method_id,
                    confirmation_method='manual',
                    confirm=True,
                    return_url=request.build_absolute_uri(reverse('checkout:order_confirmation', args=[order_id]))
                )
            elif payment_intent_id:
                # Confirm existing PaymentIntent
                intent = stripe.PaymentIntent.confirm(payment_intent_id)

            return handle_payment_intent(intent, order)

    except Exception as e:
        logger.error(f"Error in order_confirmation: {e}")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)

    return render(request, 'checkout/order_confirmation.html', {'order': order})

# Handle PaymentIntent responses and actions
def handle_payment_intent(intent, order):
    if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
        return JsonResponse({
            'requires_action': True,
            'payment_intent_client_secret': intent.client_secret
        })
    elif intent.status == 'succeeded':
        order.payment_status = 'paid'
        order.stripe_charge_id = intent.id
        order.save()
        return JsonResponse({
            'success_url': reverse('checkout:order_confirmation', args=[order.id])
        })
    else:
        return JsonResponse({
            'error': {'message': 'Invalid PaymentIntent status'}
        })

@login_required
def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email).order_by('-created_at')
    return render(request, 'checkout/order_history.html', {'orders': orders})