from django.db import models

from books.models import Books
from users.models import User, MONTHSS


ORDER_STATUS_CHOICES = (
    (0, 'В процесі обробки'),
    (1, 'Готово для отримання'),
    (2, 'Взято на читання'),
    (3, 'Протерміновано з отриманням'),
    (4, 'Протерміновано з поверненням'),
    (5, 'Повернуто'),
    (6, 'Всі книги відмовлено'),
)
BOOK_STATUS_CHOICES = (
    (0, 'Забронювати'),
    (1, 'Відмовитись'),
)

class OrderitemQueryset(models.QuerySet):
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=0)
    order_start = models.DateTimeField(blank=True, null=True)
    order_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("-id",)

    def __str__(self):
        return f"Бронювання № {self.pk} | Користувач {self.user.first_name} {self.user.last_name}"
    
    def get_formatted_time(self):
        if self.created_timestamp:
            return f"{self.created_timestamp.day} {MONTHSS[self.created_timestamp.month]} {self.created_timestamp.year}, {self.created_timestamp.hour}:{self.created_timestamp.minute:02}"
    
    def get_formatted_time_order_start(self):
        if self.order_start:
            return f"{self.order_start.day} {MONTHSS[self.order_start.month]} {self.order_start.year}, {self.order_start.hour}:{self.order_start.minute:02}"
        
    def get_formatted_time_order_end(self):
        if self.order_end:
            return f"{self.order_end.day} {MONTHSS[self.order_end.month]} {self.order_end.year}, {self.order_end.hour}:{self.order_end.minute:02}"

    def get_order_status_display(self):
        return dict(ORDER_STATUS_CHOICES).get(self.status, 'Невідомо')

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books, on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150) # if book was deleted, just in case 
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронювання")
    status = models.IntegerField(choices=BOOK_STATUS_CHOICES, default=0)

    
    class Meta:
        db_table = "order_item"
        verbose_name = "Ordered item"
        verbose_name_plural = "Ordered items"
        ordering = ("-id",)

    objects = OrderitemQueryset.as_manager()

    def __str__(self):
        return f"Книга {self.name} | Бронювання № {self.order.pk}"
    
    def get_status_display(self):
        return "Заброньовано" if self.status == 0 else "Відмовлено"