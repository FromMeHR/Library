from django import template
from django.utils.http import urlencode

from books.models import Categories

register = template.Library()

@register.simple_tag() # to register our func as templatetag
def tag_categories():
    return Categories.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs): # context - receive all context variables from views and request.GET from templates, kwargs - in catalog.html its page=page ...
    query = context['request'].GET.dict() # receive all parameters of GET request from the website, users' filters
    query.update(kwargs) # page number in the end ?on_sale=on&order_by=default&page=1
    return urlencode(query)