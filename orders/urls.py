from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('all-orders/<int:order_id>/', views.chosen_order, name='chosen_order'),
    path('overdue-orders/', views.overdue_orders, name='overdue_orders'),
    path('books-info/', views.books_info, name='books_info'),
]