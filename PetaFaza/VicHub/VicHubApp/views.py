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

def all_categories(request : HttpRequest): #comile
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }

    return render(request, 'categories.html', context)

def category_req(request: HttpRequest, category_id): #comile
    belongings = BelongsTo.objects.filter(id_category=category_id)
    category = Category.objects.get(pk=category_id)
    jokes = []
    for belonging in belongings:
        joke = Joke.objects.get(pk=belonging.id_joke.id_joke)
        jokes.append(joke)
    context= {
        "jokes" : jokes,
        "category" : category,
    }
    return render(request, 'content.html', context)
    
def joke(request: HttpRequest, joke_id): #comile
    joke = Joke.objects.get(pk=joke_id)
    comments = Comment.objects.filter(id_joke=joke)
    autor = User.objects.get(pk=joke.id_user_created.id_user)
    context = {
        "joke" : joke,
        "comments" : comments,
        "autor": autor,
    }
    return render(request, 'single_joke.html', context)