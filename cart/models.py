from django.db import models
from shirts.models import Shirt
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size_choices = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    size = models.CharField(max_length=2, choices=size_choices)

    def __str__(self):
        return f"{self.quantity} of {self.shirt.name} in size {self.size}"

    def total_price(self):
        return self.quantity * self.shirt.price
