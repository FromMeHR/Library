from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from carts.utils import get_user_carts

from books.models import Books
from carts.models import Cart

def cart_add(request):
    if request.user.is_authenticated and request.user.role != 0:
        return JsonResponse({"message": f"Ви не є читачем."})
    
    book_id = request.POST.get("book_id")
    book = Books.objects.get(id=book_id)
    response_data = {}
    
    if book.quantity < 1:
        response_data['message'] = f"Книги \"{book.name}\" немає в наявності."
    else:
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user, book=book)
        else:
            carts = Cart.objects.filter(session_key=request.session.session_key, book=book)
        
        if carts.exists():
            response_data['message'] = f"Книгу \"{book.name}\" вже було додано до кошику."
        else:
            if request.user.is_authenticated:
                Cart.objects.create(user=request.user, book=book, quantity=1)
            else:
                Cart.objects.create(session_key=request.session.session_key, book=book, quantity=1)
            response_data['message'] = f"Книгу \"{book.name}\" було додано до кошику."

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    response_data['cart_items_html'] = cart_items_html
    return JsonResponse(response_data)
    
def cart_remove(request):
    if request.user.is_authenticated and request.user.role != 0:
        return JsonResponse({"message": f"Ви не є читачем."})
    
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id = cart_id)
    quantity = cart.quantity
    cart.delete()
    
    user_cart = get_user_carts(request)
    context = {"carts": user_cart}
    
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["is_order"] = True
        
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", context, request=request)

    response_data = {
        "message": f"Книгу \"{cart.book.name}\" було прибрано з кошику.",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)