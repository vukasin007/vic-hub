from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages

from .forms import CustomUserCreationForm


def index(request: HttpRequest):
    return render(request, 'index.html')


def register_req(request: HttpRequest):
    form = CustomUserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='basic'))
            messages.success(request, 'Uspešno ste se registrovali.')
            return redirect('login')
        else:
            messages.error(request, 'Registracija nije uspela. Podaci su nevalidni.')
    return render(request, 'register.html', {
        'form': form
    })


def login_req(request: HttpRequest):
    form = AuthenticationForm(request=request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Uspešno ste se prijavili.')
                if user.groups.filter(name='basic').exists():
                    return render(request, 'logged_index.html')
                if user.groups.filter(name='moderator').exists():
                    return render(request, 'moderator/moderator_index.html')
                if user.groups.filter(name='admin').exists():
                    return render(request, 'moderator/moderator_index.html')
            else:
                messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
        else:
            messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
    return render(request, 'login.html', {
        'form': form
    })


@login_required(login_url='login')
def logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')
