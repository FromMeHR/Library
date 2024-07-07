from django.db.models import Q
from orders.models import Order, ORDER_STATUS_CHOICES

def q_search(query):
    keywords = [word for word in query.split()]
    q_objects = Q()

    for token in keywords:
        q_objects |= Q(id__icontains=token) 
    for code, status_words in ORDER_STATUS_CHOICES:
        if query.lower() in status_words.lower():
            q_objects |= Q(status=code)
    return Order.objects.filter(q_objects)
