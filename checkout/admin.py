from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_email",
        "shipping_address",
        "created_at",
        "updated_at",
    )
    search_fields = ("customer_name", "customer_email")
    list_filter = ("created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "shirt", "size", "quantity", "price")
    search_fields = ("order__customer_name", "shirt__name")
    list_filter = ("order",)
