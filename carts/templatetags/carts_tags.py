from django import template
from django.core.handlers.wsgi import WSGIRequest

from carts.utils import get_user_carts

register = template.Library()

@register.simple_tag()
def user_cart(request: WSGIRequest):
    return get_user_carts(request)
