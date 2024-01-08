from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request=request,
                                 message=f'{username} logged in successfully!'
                                 )
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('users:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request=request,
                             message=f'{user.username} registred and logged in successfully!'
                             )
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request=request,
                             message=f'{form.username} update successfully!'
                             )
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'Home - Кабинет',
        'form': form,
    }
    return render(request, 'users/profile.html', context)

# @login_required()
def users_cart(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    return render(request, 'users/users_cart.html')


@login_required()
def logout(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))
