from django.contrib import admin
from .models import Shirt, Size, ShirtSize, Review


class ShirtAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        "season",
        "home_or_away",
        "price",
        "stock",
        "featured",
    )
    list_filter = ("team", "season", "home_or_away", "featured")
    search_fields = ("name", "team", "season")


admin.site.register(Shirt, ShirtAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("shirt", "user", "rating", "created_at")
    list_filter = ("shirt", "rating")
    search_fields = ("shirt__name", "user__username")
