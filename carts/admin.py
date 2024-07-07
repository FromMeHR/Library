from django.contrib import admin
from carts.models import Cart

class CartTabAdmin(admin.TabularInline): # in users
    model = Cart
    fields = "book", "quantity", "created_timestamp"
    search_fields = "book", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "book_display", "quantity", "created_timestamp"]
    list_filter = ["created_timestamp", "user", "book__name"]
    
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Anonymous user"

    def book_display(self, obj):
        return str(obj.book.name)
    
    user_display.short_description = "User"
    book_display.short_description = "Book"