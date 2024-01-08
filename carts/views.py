from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:

    product_id = request.POST.get('product_id')
    product = Products.objects.get(pk=product_id)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        template_name='carts/includes/included_cart.html',
        context={
            'carts': user_cart,
        },
        request=request
    )

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)


def cart_change(request: WSGIRequest, product_slug) -> HttpResponseRedirect | HttpResponse:
    pass


def cart_remove(request: WSGIRequest, cart_id) -> HttpResponseRedirect | HttpResponse:
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])
