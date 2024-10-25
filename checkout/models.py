from django.db import models
from shirts.models import Shirt

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    size = models.CharField(max_length=2)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.shirt.name} in size {self.size}"