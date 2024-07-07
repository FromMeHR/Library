from django import template
from django.utils import timezone
from users.models import Abonement

register = template.Library()

@register.simple_tag()
def has_active_subscription(request):
    try:
        abonement = Abonement.objects.filter(user=request.user, abonement=True, abonement_end__gte=timezone.now()).last()
        if abonement and abonement.check_abonement():
            return True
        else:
            return False
    except Abonement.DoesNotExist:
        return False
