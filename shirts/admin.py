from django.contrib import admin
from .models import Shirt

class ShirtAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'season', 'home_or_away', 'price', 'stock')

admin.site.register(Shirt, ShirtAdmin)