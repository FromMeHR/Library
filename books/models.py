from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from books.validators import validate_is_pdf
from users.models import User
from googletrans import Translator

YEAR_CHOICES = [(i, i) for i in range(1900, timezone.now().year+1)]
LANGUAGE_CHOICES = [('англійська', 'англійська'), ('українська', 'українська')]
RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
    
    class Meta:
        db_table = 'category' # display in db
        verbose_name = 'Category' # django admin
        verbose_name_plural = 'Categories'
        ordering = ("id",)
    
    def __str__(self):
        return self.name

class Books(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='url', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='books_images', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_being_read = models.PositiveIntegerField(default=0, blank=True, null=True)
    pages = models.PositiveIntegerField(default=0, blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=50, default='українська')
    publication_year = models.IntegerField(choices=YEAR_CHOICES, default=timezone.now().year)
    date_of_issue = models.DateField(default=timezone.now)
    category = models.ManyToManyField(to=Categories)
    pdf_file = models.FileField(upload_to='pdf_files', validators=[validate_is_pdf], blank=True, null=True)

    class Meta:
        db_table = 'book'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ("id",)  # to avoid warning

    def get_absolute_url(self):
        return reverse("catalog:book", kwargs={"book_slug": self.slug})

    def __str__(self):
        return f'{self.name} Кількість: {self.quantity}'

    def display_id(self):
        return f'{self.id:05}'

    def formatted_content(self):
        return mark_safe(self.description)

@receiver(pre_save, sender=Books)
def pre_save_book_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        translator = Translator()
        translated_text = translator.translate(instance.name, dest='en').text
        instance.slug = slugify(translated_text, allow_unicode=True)
    
class WatchedLinks(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'watchedlink'
        verbose_name = 'WatchedLink'
        verbose_name_plural = 'WatchedLinks'
        
    def __str__(self):
        return f'Переглянуто pdf link книги {self.book.name}'
    
class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]