from django.db import models

class Shirt(models.Model):
    team_choices = [
        ('ARS', 'Arsenal'),
        ('CHE', 'Chelsea'),
        ('LIV', 'Liverpool'),
        ('MCI', 'Manchester City'),
        ('MUN', 'Manchester United'),
    ]

    season_choices = [
        ('2021/2022', '2021/2022'),
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
    ]

    home_or_away_choices = [
        ('Home', 'Home'),
        ('Away', 'Away'),
        ('Third', 'Third'),
    ]

    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=3, choices=team_choices)
    season = models.CharField(max_length=9, choices=season_choices)
    home_or_away = models.CharField(max_length=5, choices=home_or_away_choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='shirts/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.team} - {self.season} - {self.home_or_away})"

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
