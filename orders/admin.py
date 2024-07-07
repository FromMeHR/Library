from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "book", "name", "quantity"
    search_fields = (
        "book",
        "name",
    )
    extra = 0


class OrderTabulareAdmin(admin.TabularInline): # in users
    model = Order
    fields = (
        "status",
        "created_timestamp",
    )

    search_fields = (
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "created_timestamp",
    )

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "status",
    )
    inlines = [OrderItemTabulareAdmin]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "book", "name", "quantity"
    search_fields = (
        "order",
        "book",
        "name",
    )
    readonly_fields = ("created_timestamp",)

