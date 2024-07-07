from carts.models import Cart

def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('book') # select_related - т.к. foreignkey идёт от корзин к продуктам
    if not request.session.session_key:
        request.session.create() # if anonymous user
    return Cart.objects.filter(session_key = request.session.session_key).select_related('book')