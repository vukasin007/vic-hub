import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, permission_required

from .forms import *


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
                    return render(request, 'index.html')
                if user.groups.filter(name='moderator').exists():
                    return render(request, 'index.html')
                if user.groups.filter(name='admin').exists():
                    return render(request, 'index.html')
            else:
                messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
        else:
            messages.error(request, 'Prijava nije uspela. Podaci su nevalidni.')
    return render(request, 'login.html', {
        'form': form
    })


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
    return redirect('home')


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

        promoted: User = currrequest.id_user
        if promoted.type == "U":    # da neko ne bi skinuo adminu privilegije
            promoted.type = "M"
            promoted.save()

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
        aimedmoderator.save()
        messages.info(request, 'Uspesno oduzimanje moderator privilegija!')
    except:
        messages.error(request, 'Neuspesno oduzimanje moderator privilegija.')
    return render(request, 'index.html')    # treba render stranica za prihvatanje/odbijanje zahteva


# vukasin007
@login_required(login_url='login')
def all_requests_mod(request: HttpRequest):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        all_requests_mod = Request.objects.all()
    except:
        all_requests_mod = []
        messages.info(request, 'Neuspesno prikazivanje svih zahteva za moderatora.')
    context = {
        'all_requests_for_mod': all_requests_mod,
    }
    return render(request, 'nema stranice za to', context)  # !!!!!!!!!!!!!!!!!!!!! nema stranice za ovo


# vukasin007
@login_required(login_url='login')
def pending_jokes(request: HttpRequest):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        all_pending_jokes = Joke.objects.filter(status="P")
    except:
        all_pending_jokes = []
        messages.info(request, 'Neuspesno prikazivanje svih neodobrenih viceva.')
    context = {
        'all_pending_jokes': all_pending_jokes,
    }
    return render(request, 'new_content_review.html', context)


# vukasin007
@login_required(login_url='login')
def choose_category(request: HttpRequest, joke_id: int):
    currjoke: Joke = Joke.objects.get(pk=joke_id)
    categories = Category.objects.all()
    context = {
        "joke": currjoke,
        "categories": categories,
    }
    return render(request, "choose_category.html", context)


# vukasin007
@login_required(login_url='login')
def accept_joke(request: HttpRequest, joke_id: int, category_id: int):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        if request.method == request.GET:
            messages.error(request, 'Method nije POST')
            return render(request, 'index.html')
        currjoke: Joke = Joke.objects.get(pk=joke_id)
        currjoke.status = "A"
        currjoke.id_user_reviewed = logedmod
        currjoke.date_posted = datetime.datetime.now()
        currjoke.save()
        belongsto = BelongsTo()
        belongsto.id_joke = currjoke
        belongsto.id_category = Category.objects.get(pk=category_id)
        belongsto.save()
        messages.info(request, 'Uspesno odobravanje vica!')
    except:
        messages.error(request, 'Neuspesno odobravanje vica.')
    return redirect('pending_jokes')


# vukasin007
@login_required(login_url='login')
def reject_joke(request: HttpRequest, joke_id: int):
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        currjoke: Joke = Joke.objects.get(pk=joke_id)
        currjoke.status = "R"
        currjoke.id_user_reviewed = logedmod
        currjoke.date_posted = datetime.datetime.now()
        currjoke.save()
        messages.info(request, 'Uspesno odbijanje vica!')
    except:
        messages.error(request, 'Neuspesno odbijanje vica.')
    return redirect('pending_jokes')


# vukasin007
@login_required(login_url='login')
def delete_comment(request: HttpRequest, comment_id: int):
    logedmod: User = User.objects.get(username=request.user.get_username())
    if logedmod.type != "A" and logedmod.type != "M":  # moze i preko group privilegija
        messages.error(request, 'Nemate privilegije.')
        return render(request, 'index.html')
    if request.method == request.GET:
        messages.error(request, 'Method nije POST')
        return render(request, 'index.html')
    currkom: Comment = Comment.objects.get(pk=comment_id)
    currkom.status = "D"
    currkom.save()
    messages.info(request, 'Uspesno brisanje komentara!')
    return redirect('home')


# vukasin007
@login_required(login_url='login')
def add_category_req(request: HttpRequest):
    logedmod: User = User.objects.get(username=request.user.get_username())
    if logedmod.type != "A" and logedmod.type != "M":  # moze i preko group privilegija
        messages.error(request, 'Nemate privilegije.')
        return render(request, 'index.html')
    forma: AddNewCategoryForm = AddNewCategoryForm(data=request.POST or None)
    if forma.is_valid():
        nova_kategorija = forma.cleaned_data.get('newCategoryName')
        kategorija: Category = Category()
        kategorija.name = nova_kategorija
        kategorija.save()
        messages.info(request, 'Uspesno kreiranje nove kategorije!')
    context = {
        'addCategoryForm': forma,
    }
    return render(request, 'stranica za dodavanje kategorije', context)  # fali stranica za dodavanje kategorije


# vukasin007
@login_required(login_url='login')
def grade_joke(request: HttpRequest, joke_id: int, grade: int):
    if request.method == request.GET:
        messages.error(request, 'Method nije POST')
        return render(request, 'index.html')
    curruser: User = User.objects.get(username=request.user.get_username())
    if grade < 1:
        grade = 1
    elif grade > 5:
        grade = 5
    flag_already_graded: bool = False
    ocene_usera = Grade.objects.filter(id_user=curruser)
    for ocena in ocene_usera:
        if ocena.id_joke == joke_id:
            ocena.grade = grade
            ocena.save()
            flag_already_graded = True
            break
    if not flag_already_graded:
        ocena: Grade = Grade()
        ocena.id_joke = Joke.objects.get(pk=joke_id)
        ocena.id_user = curruser
        ocena.grade = grade
        ocena.save()
    messages.info(request, 'Ocenili ste vic sa ocenom: ' + str(grade))
    try:
        currjoke = Joke.objects.get(pk=joke_id)
        firstBelongsTo = BelongsTo.objects.filter(id_joke=currjoke).first()
        firstcategory = firstBelongsTo.id_category
        return redirect('category', category_id=firstcategory.id_category)    # predji u prikaz iste kategorije
    except:
        return redirect('all_categories')


def category_req(request: HttpRequest, category_id):  # comile
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