from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Q, Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse
from carts.models import Cart
from orders.forms import BookStatusForm
from orders.models import BOOK_STATUS_CHOICES, Order, OrderItem

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm, AbonementForm
from users.models import Abonement
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Count
from django.http import JsonResponse


def login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form:
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password) # check in db
            
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f'{user.username} успішно авторизований')
                
                if user.role != 1 and session_key:
                    old_carts = Cart.objects.filter(user=user)
                    if old_carts.exists():
                        old_carts.delete()
                    Cart.objects.filter(session_key=session_key).update(user=user)
                
                redirect_page = request.POST.get('next', None) # if not authorized user try to visit profile
                if redirect_page and redirect_page != reverse('user:logout'):
                    return redirect(request.POST.get('next')) # '/user/profile/'

                return redirect(reverse('main:index'))
    else:
        form = UserLoginForm()
        
    context = {
        'title': 'Log in',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            session_key = request.session.session_key
            
            user = form.instance
            auth.login(request, user)
                        
            if user.role != 1 and session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                
            messages.success(request, f'{user.username} успішно зареєстрований')
            return redirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
        
    context = {
        'title': 'Registration',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Профіль успішно оновлено')
            return redirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
        
    orders = Order.objects.filter(user=request.user).prefetch_related( # prefetch_related -  т.к. foreignkey идёт от OrderItem к Order (в обратном порядке (не select))
    Prefetch(
        "orderitem_set", # additional queryset
        queryset=OrderItem.objects.select_related("book"),
    )).order_by("-id")
        
    context = {
        'title': 'Profile',
        'form': form,
        'orders': orders,
        'status_choices': dict(BOOK_STATUS_CHOICES),
    }
    return render(request, 'users/profile.html', context)

@login_required
def admin_panel(request):
    if request.user.role != 1:
        return render(request, 'includes/404.html', status=404)
    return render(request, 'users/admin_panel.html')

@login_required
def get_chart_data(request):
    timeframe = request.GET.get('timeframe', 'month')
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        chart_data = (
            OrderItem.objects
            .filter(created_timestamp__date__gte=start_date, created_timestamp__date__lte=end_date)
            .exclude(status=1)
            .extra(select={'day': "to_char(created_timestamp, 'DD-MM-YYYY')"})
            .values('day')
            .annotate(count=Count('id'))
        )
        labels = [(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days + 1)]
    else:
        today = timezone.now().date()
        if timeframe == 'month':
            chart_data = (
                OrderItem.objects
                .filter(created_timestamp__gte=today - timedelta(days=30), created_timestamp__lte=today)
                .exclude(status=1)
                .extra(select={'day': "to_char(created_timestamp, 'DD-MM-YYYY')"})
                .values('day')
                .annotate(count=Count('id'))
            )
            labels = [(today - timedelta(days=i)).strftime('%d-%m-%Y') for i in range(30, -1, -1)]
        else:
            chart_data = (
                OrderItem.objects
                .filter(created_timestamp__year__gte=today.year - 1)
                .exclude(status=1)
                .extra(select={'month': "to_char(created_timestamp, 'MM-YYYY')"})
                .values('month')
                .annotate(count=Count('id'))
            )
            labels = [(today - timedelta(days=30 * i)).strftime('%m-%Y') for i in range(12, -1, -1)]

    counts_by_date = {}
    for item in chart_data:
        key = item.get('day' if timeframe == 'month' or timeframe == 'custom' else 'month')
        if key:
            counts_by_date[key] = item['count']    
    data = [counts_by_date.get(label, 0) for label in labels]
    return JsonResponse({'labels': labels, 'data': data})

@login_required
def update_book_status(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    if request.method == 'POST':
        form = BookStatusForm(request.POST)
        if form.is_valid():
            order_item_id = form.cleaned_data['order_item_id']
            new_status = form.cleaned_data['status']
            
            order_item = OrderItem.objects.get(id=order_item_id)
            if order_item.order.status == 0:
                order_item.status = new_status
                order_item.save()
                messages.success(request, 'Статус книги успішно змінено')
            else:
                messages.error(request, 'Неможливо змінити статус книги, так як статус бронювання не "В процесі обробки"')
    return redirect(request.META['HTTP_REFERER'])

def users_cart(request):
    return render(request, 'users/users_cart.html')

@login_required
def logout(request):
    messages.warning(request, f'{request.user.username} вийшов')
    auth.logout(request)
    return redirect(reverse('main:index'))


@login_required
def abonement_form(request):
    if request.user.get_active_abonement(request.user):
        messages.warning(request, 'У вас вже є активний абонемент.')
        return redirect(reverse('main:index'))
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    if request.method == 'POST':
        form = AbonementForm(request.POST)
        if form.is_valid():
            user = request.user
            radius = form.cleaned_data['radius']
            price = 100 if radius == '1_month' else 500
            amount_of_days = 30 if radius == '1_month' else 365
            payment_status = 0

            abonement_start = timezone.now()
            abonement_end = abonement_start + timezone.timedelta(days=amount_of_days)

            abonement = Abonement.objects.create(
                user=user,
                abonement=True,
                abonement_start=abonement_start,
                abonement_end=abonement_end,
                price=price,
                amount_of_days=amount_of_days,
                payment_status=payment_status,
            )
            abonement.save()
            messages.success(request, 'Абонемент успішно оформлено.')
            return redirect(reverse('main:index'))
    else:
        form = AbonementForm()

    context = {
        'form': form,
    }
    return render(request, 'users/abonement_create.html', context)

@login_required
def abonement_details(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    user = request.user
    active_abonement = user.get_active_abonement(user)
    all_abonements = user.abonement_set.all()
    context = {
        'active_abonement': active_abonement,
        'all_abonements': all_abonements,
    }
    return render(request, 'users/abonement_details.html', context)