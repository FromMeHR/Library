from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


ROLE_CHOICES = (
    (0, 'reader'),
    (1, 'administrator'),
)
PAYMENT_STATUS_CHOICES = (
    (0, 'Вдало'),
    (1, 'Невдало'),
)
MONTHSS = {
    1: 'січня', 2: 'лютого', 3: 'березня',
    4: 'квітня', 5: 'травня', 6: 'червня',
    7: 'липня', 8: 'серпня', 9: 'вересня',
    10: 'жовтня', 11: 'листопада', 12: 'грудня'
}


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField(upload_to='books_images', blank=True, null=True, verbose_name='Avatar')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def get_active_abonement(self, user):
        return user.abonement_set.filter(abonement=True, abonement_end__gte=timezone.now()).first()
        
class Abonement(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    abonement = models.BooleanField(default=False)
    abonement_start = models.DateTimeField(blank=True, null=True)
    abonement_end = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount_of_days = models.PositiveIntegerField()
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=1)

    def __str__(self):
        return f"Abonement for {self.user.username}"
    
    def check_abonement(self):
        if self.abonement and self.abonement_start <= timezone.now() <= self.abonement_end:
            return True
        else:
            return False
        
    def get_formatted_time(self):
        return f"{self.abonement_start.day} {MONTHSS[self.abonement_start.month]} {self.abonement_start.year}, {self.abonement_start.hour}:{self.abonement_start.minute:02}"
    
    def get_payment_status_display(self):
        return dict(PAYMENT_STATUS_CHOICES).get(self.payment_status, 'Невідомо')

@receiver(post_save, sender=Abonement)
def update_abonements(sender, instance, created, **kwargs):
    if created:
        Abonement.objects.filter(user=instance.user).exclude(pk=instance.pk).update(abonement=False)