from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import *


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
    return render(request, 'login.html')

def all_categories(request : HttpRequest):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'categories.html', context)
