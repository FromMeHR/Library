from django.db import models

from books.models import Books
from users.models import User

class CartQueryset(models.QuerySet):
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ("id",)
        
    objects = CartQueryset().as_manager() # + own methods to objects

    def __str__(self):
        if self.user: 
            return f'Кошик {self.user.username} | Книга {self.book.name} | Кількість {self.quantity}'
        return f'Анонімний кошик | Книга {self.book.name} | Кількість {self.quantity}'