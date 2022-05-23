from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages

from .models import *
from .forms import CustomUserCreationForm


def is_guest(user):
    return not user.is_authenticated


def is_moderator(user):
    return user.groups.filter(name='moderator').exists() or user.groups.filter(name='admin').exists()


def is_admin(user):
    return user.groups.filter(name='admin').exists()


def index(request: HttpRequest):
    return render(request, 'index.html')


@user_passes_test(is_guest, login_url='home', redirect_field_name=None)
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


@user_passes_test(is_guest, login_url='home', redirect_field_name=None)
def login_req(request: HttpRequest):
    form = AuthenticationForm(request=request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if (user is not None) and (user.status == 'A'):
                login(request, user)
                messages.success(request, 'Uspešno ste se prijavili.')
                return redirect('home')
            else:
                messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
        else:
            messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
    return render(request, 'login.html', {
        'form': form
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home', redirect_field_name=None)
def admin_all_users(request: HttpRequest):
    return render(request, 'admin_all_users.html', {
        'users': User.objects.filter(Q(type='U') | Q(type='M'))
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home', redirect_field_name=None)
def delete_user_admin(req: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    user.status = 'B'
    user.subscribed = 'N'
    user.save()
    for request in Request.objects.filter(id_user=user):
        if request.status == 'P':
            request.status = 'R'
            request.id_user_reviewed = req.user
            request.save()
    for grade in Grade.objects.filter(id_user=user):
        grade.delete()
    for comment in Comment.objects.filter(id_user=user):
        comment.status = 'D'
        comment.save()
    for joke in Joke.objects.filter(id_user_created=user):
        if joke.status == 'P':
            joke.id_user_reviewed = req.user
        joke.status = 'D'
        joke.save()
        for comment in Comment.objects.filter(id_joke=joke):
            comment.status = 'D'
            comment.save()
    messages.success(req, f'Korisnik {user.username} je uspešno obrisan.')
    return redirect('admin_all_users')


def all_categories(request : HttpRequest): #comile
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }

    return render(request, 'categories.html', context)


# vukasin007
def logout_req(request: HttpRequest):
    try:
        logout(request)
        messages.info(request, 'Uspesna odjava!')
    except:
        messages.error(request, 'Niste prijavljeni.')
    return render(request, 'index.html')


# vukasin007
@login_required(login_url='login')
def subscribe_to_bilten(request: HttpRequest):
    try:
        curruser = User.objects.get(username=request.user.get_username())
        curruser.subscribed = "Y"
        curruser.save()
        messages.info(request, 'Uspesna prijava na bilten!')
    except:
        messages.error(request, 'Neuspesna prijava na bilten.')
    return render(request, 'index.html')


# vukasin007
@login_required(login_url='login')
def unsubscribe_from_bilten(request: HttpRequest):
    try:
        curruser = User.objects.get(username=request.user.get_username())
        curruser.subscribed = "N"
        curruser.save()
        messages.info(request, 'Uspesna odjava sa biltena!')
    except:
        messages.error(request, 'Neuspesna odjava sa biltena.')
    return render(request, 'index.html')


# vukasin007
@login_required(login_url='login')
def request_mod(request: HttpRequest):
    try:
        curruser = User.objects.get(username=request.user.get_username())
        currrequest: Request = Request()
        currrequest.status = "P"
        currrequest.user = curruser
        currrequest.save()
        messages.info(request, 'Uspesno formiran zahtev za moderatora!')
    except:
        messages.error(request, 'Neuspesan zahtev za moderatora.')
    return render(request, 'index.html')


# vukasin007
@login_required(login_url='login')
def accept_mod_request(request: HttpRequest, request_id: int):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        currrequest: Request = Request.objects.get(pk=request_id)
        currrequest.status = "A"
        currrequest.id_user_reviewed = logedmod
        currrequest.save()
        messages.info(request, 'Uspesno prihvatanje zahteva za moderatora!')
    except:
        messages.error(request, 'Neuspesno prihvatanje zahteva za moderatora.')
    return render(request, 'index.html')    # treba render stranica za prihvatanje/odbijanje zahteva


# vukasin007
@login_required(login_url='login')
def reject_mod_request(request: HttpRequest, request_id: int):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        currrequest: Request = Request.objects.get(pk=request_id)
        currrequest.status = "R"
        currrequest.id_user_reviewed = logedmod
        currrequest.save()
        messages.info(request, 'Uspesno odbijanje zahteva za moderatora!')
    except:
        messages.error(request, 'Neuspesno odbijanje zahteva za moderatora.')
    return render(request, 'index.html')    # treba render stranica za prihvatanje/odbijanje zahteva


# vukasin007
@login_required(login_url='login')
def remove_mod(request: HttpRequest, user_id: int):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        aimedmoderator: User = User.objects.get(pk=user_id)
        aimedmoderator.type = "U"
        # promeni grupu usera, kao preko django admina
        #   #   #
        #  here #
        #   #   #
        aimedmoderator.save()
        messages.info(request, 'Uspesno odbijanje zahteva za moderatora!')
    except:
        messages.error(request, 'Neuspesno odbijanje zahteva za moderatora.')
    return render(request, 'index.html')    # treba render stranica za prihvatanje/odbijanje zahteva


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


@login_required(login_url='login')
def add_joke(request: HttpRequest):
    if request.method == 'POST':
        title = request.POST['joke_title']
        content = request.POST['joke_content']
        new_joke = Joke()
        new_joke.title=title
        new_joke.content=content
        new_joke.id_user_created = request.user
        new_joke.status = "P"
        new_joke.save()
    
    return render(request, "add_joke.html")


@login_required(login_url='login')
def profile(request: HttpRequest):
    return render(request, 'profile.html')


@login_required(login_url='login')
def add_comment(request: HttpRequest, joke_id):
    joke = Joke.objects.get(pk=joke_id)
    context = {
        "joke": joke
    }
    if request.method == "POST":
        content = request.POST["comment_content"]
        new_comment = Comment()
        new_comment.id_joke=joke
        new_comment.id_user = request.user
        new_comment.content = content
        jokes = Comment.objects.filter(id_joke=joke)
        number = jokes.count()+1
        new_comment.ordinal_number = number
        new_comment.status = 'A'
        new_comment.save()

    return render(request, "add_comment.html", context)
