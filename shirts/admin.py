from django.contrib import admin
from .models import Shirt, Size, ShirtSize

class ShirtAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'season', 'home_or_away', 'price', 'stock', 'featured')
    list_filter = ('team', 'season', 'home_or_away', 'featured')
    search_fields = ('name', 'team', 'season')

admin.site.register(Shirt, ShirtAdmin)