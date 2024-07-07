from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('book/<slug:book_slug>/', views.book, name='book'),
    path('watched/watched-links/', views.watched_links, name='watched_links'), 
    path('watched/check-watched-link/', views.check_watched_link, name='check_watched_link'),
    path('book-form/create-book/', views.create_book, name="create_book"),
    path('book-form/<slug:book_slug>/', views.update_book, name="update_book"),
    path('book/update-comment/<int:comment_id>/', views.update_comment, name='update_comment'),
]