from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, permission_required


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


def all_categories(request: HttpRequest):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    
    return render(request, 'categories.html', context)


def logout_req(request: HttpRequest):
    try:
        logout(request)
        messages.info(request, 'Uspesna odjava!')
    except:
        messages.error(request, 'Niste prijavljeni.')
    return render(request, 'index.html')


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
