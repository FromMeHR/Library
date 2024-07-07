from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
    path('abonement/', views.abonement_form, name='abonement_form'),
    path('abonement/details/', views.abonement_details, name='abonement_details'),
    path('update-book-status/', views.update_book_status, name='update_book_status'),
    path('get-chart-data/', views.get_chart_data, name='get_chart_data'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
