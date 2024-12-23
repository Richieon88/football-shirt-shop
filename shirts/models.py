from django.db import models
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.contrib.auth.models import User

class Shirt(models.Model):
    home_or_away_choices = [
        ('Home', 'Home'),
        ('Away', 'Away'),
        ('Third', 'Third'),
    ]

    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    season = models.CharField(max_length=9)
    home_or_away = models.CharField(max_length=5, choices=home_or_away_choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = CloudinaryField('image')
    stock = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.team} - {self.season} - {self.home_or_away})"

    def get_absolute_url(self):
        return reverse('shirts:shirt_detail', args=[str(self.pk)])

class Size(models.Model):
    size_choices = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    size = models.CharField(max_length=2, choices=size_choices, unique=True)

    def __str__(self):
        return self.size

class ShirtSize(models.Model):
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name='sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='shirts')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shirt.name} - {self.size.size}"

class Review(models.Model):
    shirt = models.ForeignKey('Shirt', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shirt', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.shirt.name} ({self.rating}/5)"