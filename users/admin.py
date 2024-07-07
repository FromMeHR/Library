from django.contrib import admin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User, Abonement
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username','first_name','last_name','email',)
    list_display = ('username','first_name','last_name','email',)
    search_fields = ('username','first_name','last_name','email',)
    
    inlines = [CartTabAdmin, OrderTabulareAdmin]
    
@admin.register(Abonement)
class AbonementAdmin(admin.ModelAdmin):
    list_filter = ('abonement','price','amount_of_days','payment_status',)
    list_display = ('id','abonement','price','amount_of_days','payment_status',)
    search_fields = ('price',)
