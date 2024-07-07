from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.urls import reverse
from django.utils import timezone
from orders.forms import CreateOrderForm, UpdateOrderForm
from carts.models import Cart
from orders.models import Order, OrderItem
from orders.utils import q_search

@login_required
def create_order(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    if not request.user.abonement_set.filter(abonement=True, abonement_end__gte=timezone.now()).exists():
        messages.warning(request, 'Для оформлення бронювання книг потрібний активний абонемент.')
        return redirect(reverse('users:abonement_form'))
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic(): # error => cancel all transactions
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                        )
                        for cart_item in cart_items:
                            book=cart_item.book
                            name=cart_item.book.name
                            quantity=cart_item.quantity

                            if book.quantity < quantity:
                                raise ValidationError(f'Недостатня кількість книг {name} в бібліотеці\
                                                       Доступно - {book.quantity}')
                            OrderItem.objects.create(
                                order=order,
                                book=book,
                                name=name,
                                quantity=quantity,
                            )
                            book.save()

                        cart_items.delete()
                        messages.success(request, 'Бронювання в процесі обробки!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect('orders:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Create an order',
        'form': form,
        'is_order': True,
    }
    return render(request, 'orders/create_order.html', context=context)

@login_required
def books_info(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    user = request.user
    status = request.GET.get('status')

    if status == 'reserved':
        order_items = OrderItem.objects.filter(order__user=user, order__status=0).exclude(status=1)
    elif status == 'read':
        order_items = OrderItem.objects.filter(order__user=user, order__status=5).exclude(status=1)
    else:
        order_items = OrderItem.objects.filter(order__user=user, order__status=2).exclude(status=1)

    context = {
        'order_items': order_items,
        'status': status,
    }
    return render(request, 'orders/books_info.html', context=context)

@login_required
def all_orders(request):
    if request.user.role != 1:
        return render(request,'includes/404.html', status=404) 
    all_reader_orders = Order.objects.all()
    
    query = request.GET.get('q', None)
    if query:
        all_reader_orders = q_search(query)

    context = {
        'all_reader_orders': all_reader_orders,
    }
    return render(request, 'orders/all_orders.html', context=context)

@login_required
def chosen_order(request, order_id):
    if request.user.role != 1:
        return render(request,'includes/404.html', status=404) 
    
    order = get_object_or_404(Order, id=order_id)
    user_of_order = order.user
    orders = Order.objects.filter(id=order_id).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("book"),
        )
    ).order_by("-id")
    old_status = order.status

    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_status = form.cleaned_data['status']

                    if (old_status in [0, 1, 3]) and (new_status == 2):
                        for item in order.orderitem_set.all():
                            if item.status != 1:
                                book = item.book
                                if book.quantity >= item.quantity:
                                    book.quantity -= item.quantity # 1
                                    book.is_being_read += item.quantity
                                    book.save()
                                else:
                                    raise Exception(f'Недостатня кількість книг "{book.name}" на складі')
                            
                    elif (old_status in [2, 4]) and (new_status == 5):
                        for item in order.orderitem_set.all():
                            if item.status != 1:
                                book = item.book
                                if book.is_being_read >= item.quantity:
                                    book.quantity += item.quantity
                                    book.is_being_read -= item.quantity
                                    book.save()
                                else:
                                    raise Exception(f'Недостатня кількість книг "{book.name}" в процесі читання')
                            
                    form.save()
                    messages.success(request, 'Дані бронювання успішно оновлено!')
                    return redirect(reverse('orders:chosen_order', args=[order_id]))
            except Exception as e:
                messages.error(request, f'Помилка при оновленні бронювання: {str(e)}')
                return redirect(reverse('orders:chosen_order', args=[order_id]))
    else:
        form = UpdateOrderForm(instance=order)
    
    context = {
        'order': order,
        'user_of_order': user_of_order,
        'orders': orders,
        'form': form,
    }
    return render(request, 'orders/chosen_order.html', context=context)


@login_required
def overdue_orders(request):
    if request.user.role != 1:
        return render(request, 'includes/404.html', status=404)

    status = request.GET.get('status')

    if status == 'return':
        overdue_orders = Order.objects.filter(status=4) | Order.objects.filter(status=2, order_end__lt=timezone.now())
    else:
        overdue_orders = Order.objects.filter(status=3) | Order.objects.filter(status=1, created_timestamp__lte=timezone.now()-timezone.timedelta(days=2))

    context = {
        'overdue_orders': overdue_orders,
    }
    return render(request, 'orders/overdue_orders.html', context=context)

