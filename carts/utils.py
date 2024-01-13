from django.core.handlers.wsgi import WSGIRequest

from carts.models import Cart


def get_user_carts(request: WSGIRequest):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
