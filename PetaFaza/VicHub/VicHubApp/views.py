import datetime
import re
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages

from .models import *
from .forms import *


def is_guest(user):
    """
    funkcija proverava da li je korisnik ulogovan na sistem
    :param user:User
    :return boolean
    """
    return not user.is_authenticated


def is_moderator(user):
    """
    funkcija proverava da li je ulogovani korisnik moderator ili administrator
    :param user:User
    :return boolean
    """
    return user.type=="M" or user.type=="A"
        #user.groups.filter(name='moderator').exists() or user.groups.filter(name='admin').exists()


def is_admin(user):
    """
    funkcija proverava da li je ulogovani korisnik administrator
    :param user:User
    :return boolean
    """
    return user.type=="A"
        #user.groups.filter(name='admin').exists()


def index(request: HttpRequest):
    """
    funkcija vraća početnu stranicu sajta
    :param request:HttpRequest
    :return HttpResponse
    """
    return render(request, 'index.html')


@user_passes_test(is_guest, login_url='home', redirect_field_name=None)
def register_req(request: HttpRequest):
    """
    funkcija vraća stranicu za registraciju i obrađuje zahtev za registraciju
    :param request:HttpRequest
    :return HttpResponse
    """
    form = CustomUserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='basic'))
            messages.success(request, 'Uspešno ste se registrovali.')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registracija nije uspela. Podaci su nevalidni.')
    return render(request, 'register.html', {
        'form': form
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home', redirect_field_name=None)
def register_admin_req(request: HttpRequest):
    """
    funkcija vraća stranicu za kreiranje korisnika od strane admina i obrađuje zahtev za kreiranje korisnika
    :param request:HttpRequest
    :return HttpResponse
    """
    form = CustomUserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name=request.POST.get('type')))
            if request.POST.get('type') == 'moderator':
                user.type = 'M'
                user.save()
            messages.success(request, 'Uspešno ste kreirali novog korisnika.')
            return redirect('home')
        else:
            messages.error(request, 'Dodavanje korisnika nije uspelo. Podaci su nevalidni.')
    return render(request, 'register_admin.html', {
        'form': form
    })


@user_passes_test(is_guest, login_url='home', redirect_field_name=None)
def login_req(request: HttpRequest):
    """
    funkcija vraća stranicu za logovanje i obrađuje zahtev za logovanje
    :param request:HttpRequest
    :return HttpResponse
    """
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
    """
    funkcija vraća stranicu sa svim korisnicima, dostupna je samo adminu
    :param request:HttpRequest
    :return HttpResponse
    """
    return render(request, 'admin_all_users.html', {
        'users': User.objects.filter(Q(type='U') | Q(type='M')).filter(status="A")
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home', redirect_field_name=None)
def delete_user_admin(req: HttpRequest, user_id: int):
    """
    funkcija omogućava adminu da obriše korisnika i vraća mu stranicu sa pregledom svih korisnika
    :param request:HttpRequest, user_id:int
    :return HttpResponse
    """
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


@login_required(login_url='login')
@user_passes_test(is_moderator, login_url='home', redirect_field_name=None)
def delete_joke(request: HttpRequest, joke_id: int):
    """
    funkcija briše odabrani vic i vraća početnu stranicu
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    if request.method == 'GET':
        messages.error(request, 'Method nije POST')
        return render(request, 'index.html')
    joke = Joke.objects.get(pk=joke_id)
    if joke.status == 'P':
        joke.id_user_reviewed = request.user
    joke.status = 'D'
    joke.save()
    for comment in Comment.objects.filter(id_joke=joke):
        comment.status = 'D'
        comment.save()
    messages.success(request, 'Vic je uspešno obrisan.')
    return redirect('home')


def all_categories(request : HttpRequest):
    """
    funkcija vraća stranicu sa svim kategorijama
    :param request:HttpRequest
    :return HttpResponse
    """
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'categories.html', context)


# vukasin007
def logout_req(request: HttpRequest):
    """
    funkcija odjavljue korisnika i vraća početnu stranicu
    :param request:HttpRequest
    :return HttpResponse
    """
    try:
        logout(request)
        messages.info(request, 'Uspesna odjava!')
    except:
        messages.error(request, 'Niste prijavljeni.')
    return redirect('home')


# vukasin007
@login_required(login_url='login')
def subscribe_to_bilten(request: HttpRequest):
    """
    funkcija prijavljuje korisnika na bilten i vraća stranicu sa podacima korisnika
    :param request:HttpRequest
    :return HttpResponse
    """
    try:
        curruser = User.objects.get(username=request.user.get_username())
        curruser.subscribed = "Y"
        curruser.save()
        messages.info(request, 'Uspesna prijava na bilten!')
    except:
        messages.error(request, 'Neuspesna prijava na bilten.')
    return redirect('profile')


# vukasin007
@login_required(login_url='login')
def unsubscribe_from_bilten(request: HttpRequest):
    """
    funkcija odjavljue korisnika sa biltena i vraća stranicu sa podacima korisnika
    :param request:HttpRequest
    :return HttpResponse
    """
    try:
        curruser = User.objects.get(username=request.user.get_username())
        curruser.subscribed = "N"
        curruser.save()
        messages.info(request, 'Uspesna odjava sa biltena!')
    except:
        messages.error(request, 'Neuspesna odjava sa biltena.')
    return redirect('profile')


# vukasin007
@login_required(login_url='login')
def request_mod(request: HttpRequest):
    """
    funkcija šalje zahtev ze promociju u moderatora i vraća početnu stranicu
    :param request:HttpRequest
    :return HttpResponse
    """
    try:
        if is_moderator(request.user):
            messages.error(request, "Nemate pravo na ovu akciju")
            return redirect('home')
        requests = Request.objects.filter(id_user=request.user)
        for request1 in requests:
            if request1.status == "P" or request1 == "A":
                messages.warning(request, "Vec ste poslali zahtev")
                return redirect('home')

        currrequest: Request = Request()
        currrequest.status = "P"
        currrequest.id_user = User.objects.get(username=request.user.get_username())
        currrequest.save()
        messages.info(request, 'Uspesno formiran zahtev za moderatora!')
    except:
        messages.error(request, 'Neuspesan zahtev za moderatora.')
    return redirect('home')


# vukasin007
@login_required(login_url='login')
def accept_mod_request(request: HttpRequest, request_id: int):
    """
    funkcija prihvata zahtev za moderatora koji ima identifikator request_id
    :param request:HttpRequest , request_id:int
    :return HttpResponse
    """
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
    """
    funkcija odbija zahtev za moderatora koji ima identifikator request_id
    :param request:HttpRequest , request_id:int
    :return HttpResponse
    """
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
    """
    funkcija oduzima moderatorske privilegije korisniku koji ima identifikator user_id
    :param request:HttpRequest , user_id:int
    :return HttpResponse
    """
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        aimedmoderator: User = User.objects.get(pk=user_id)
        if aimedmoderator.type != "M":
            messages.error(request, 'Korisnik kojem oduzimate privilegije nije moderator.')
            return render(request, 'index.html')
        aimedmoderator.type = "U"
        aimedmoderator.save()
        messages.info(request, 'Uspesno oduzimanje moderator privilegija!')
    except:
        messages.error(request, 'Neuspesno oduzimanje moderator privilegija.')
    return render(request, 'index.html')    # treba render stranica za prihvatanje/odbijanje zahteva


# vukasin007
@login_required(login_url='login')
@user_passes_test(is_moderator, login_url='home', redirect_field_name=None)
def all_requests_mod(request: HttpRequest):
    """
    funkcija vraća stranicu sa svim zahtevima za moderatora
    :param request:HttpRequest
    :return HttpResponse
    """
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
    return render(request, 'admin_all_requests_mod.html', context)


# vukasin007
@login_required(login_url='login')
def pending_jokes(request: HttpRequest):
    """
    funkcija vraća stranicu sa svim vicevima koji iščekuju da budu odobreni
    :param request:HttpRequest
    :return HttpResponse
    """
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
    """
    funkcija vraća stranicu za odabir kategorije vica koji se odobrava
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    #if request.method == 'GET':
       # messages.error(request, 'Method nije POST')
       # return render(request, 'index.html')
    if is_moderator(request.user) == False:
        messages.error(request, 'Nemate privilegije')
        return render(request, 'index.html')
    currjoke: Joke = Joke.objects.get(pk=joke_id)
    categories = Category.objects.all()
    autor = User.objects.get(pk=currjoke.id_user_created.id_user)
    context = {
        "joke": currjoke,
        "categories": categories,
        "autor": autor
    }
    return render(request, "choose_category.html", context)


@login_required(login_url='login')
@user_passes_test(is_moderator, login_url='home', redirect_field_name=None)
def add_category(request: HttpRequest):
    return redirect('all_categories')


# vukasin007
@login_required(login_url='login')
def accept_joke(request: HttpRequest, joke_id: int):
    """
    funkcija odobrava vic sa identifikatorom joke_id i vraća stranicu sa neodobrenim vicevima
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":   # moze i preko group privilegija
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        if request.method == 'GET':
            messages.error(request, 'Method nije POST')
            return render(request, 'index.html')

        kategorije = request.POST.getlist('kategorija')

        if kategorije.__len__() == 0:
            messages.error(request,"Niste odabrali kategoriju")
            return redirect("choose_category", joke_id=joke_id)

        currjoke: Joke = Joke.objects.get(pk=joke_id)
        currjoke.status = "A"
        currjoke.id_user_reviewed = logedmod
        currjoke.date_posted = datetime.datetime.now()
        currjoke.save()

        for id_kat in kategorije:
            id_cat = int(id_kat)
            category = Category.objects.get(pk=id_cat)

            belongsto = BelongsTo()
            belongsto.id_joke = currjoke
            belongsto.id_category = category
            belongsto.save()

        messages.info(request, 'Uspesno odobravanje vica!')
    except:
        messages.error(request, 'Neuspesno odobravanje vica.')
    return redirect('pending_jokes')


# vukasin007
@login_required(login_url='login')
def reject_joke(request: HttpRequest, joke_id: int):
    """
    funkcija odbija vic sa identifikatorom joke_id i vraća stranicu sa neodobrenim vicevima
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    try:
        logedmod: User = User.objects.get(username=request.user.get_username())
        if logedmod.type != "A" and logedmod.type != "M":
            messages.error(request, 'Nemate privilegije.')
            return render(request, 'index.html')
        if request.method == 'GET':
            messages.error(request, 'Method nije POST')
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
    """
    funkcija uklanja komentar sa identifikatorom comment_id i vraća stranicu sa vicem na koji se komentar odnosio
    :param request:HttpRequest, comment_id:int
    :return HttpResponse
    """
    logedmod: User = User.objects.get(username=request.user.get_username())
    if logedmod.type != "A" and logedmod.type != "M":  # moze i preko group privilegija
        messages.error(request, 'Nemate privilegije.')
        return render(request, 'index.html')
    if request.method == 'GET':
        messages.error(request, 'Method nije POST')
        return render(request, 'index.html')
    currkom: Comment = Comment.objects.get(pk=comment_id)
    currkom.status = "D"
    currkom.save()
    id_joke = int(request.POST['id_joke'])
    messages.info(request, 'Uspesno brisanje komentara!')
    return redirect('joke', joke_id=id_joke)


# vukasin007
@login_required(login_url='login')
@user_passes_test(is_moderator, login_url='home', redirect_field_name=None)
def add_category_req(request: HttpRequest):
    """
    funkcija vraća stranicu za kreiranje nove kategorije i kreira novu kategoriju
    :param request:HttpRequest
    :return HttpResponse
    """
    logedmod: User = User.objects.get(username=request.user.get_username())
    if logedmod.type != "A" and logedmod.type != "M":  # moze i preko group privilegija
        messages.error(request, 'Nemate privilegije.')
        return render(request, 'index.html')
    forma: AddNewCategoryForm = AddNewCategoryForm(data=request.POST or None)
    if forma.is_valid():
        try:
            nova_kategorija = forma.cleaned_data.get('Naziv')
            if (nova_kategorija.__len__() < 1):
                messages.warning(request, "Niste uneli naziv kategorije")
                return redirect("add_category")
            kategorija: Category = Category()
            kategorija.name = nova_kategorija
            kategorija.save()
            messages.info(request, 'Uspesno kreiranje nove kategorije!')
        except:
            messages.info(request, 'Neuspesno kreiranje nove kategorije.')
        return redirect('all_categories')
    context = {
        'addCategoryForm': forma,
    }
    return render(request, 'add_category.html', context)


# vukasin007
@login_required(login_url='login')
def grade_joke(request: HttpRequest, joke_id: int):
    """
    funkcija ocenjuje vic sa identifikatorom joke_id i cuva ocenu
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    if request.method == 'GET':
        messages.error(request, 'Method nije POST')
        return render(request, 'index.html')
    curruser: User = User.objects.get(username=request.user.get_username())
    joke_curr = Joke.objects.get(pk=joke_id)

    if joke_curr.id_user_created.username == request.user.get_username():
        messages.warning(request, "Ne možete oceniti svoj vic")
        return redirect("joke", joke_id=joke_id)

    grade = int(request.POST['grade'])
    if grade < 1:
        grade = 1
    elif grade > 5:
        grade = 5

    flag_already_graded: bool = False
    ocene_usera = Grade.objects.filter(id_user=curruser)
    for ocena in ocene_usera:
        if ocena.id_joke.id_joke == joke_id:
            ocena.grade = grade
            ocena.date = datetime.datetime.now()
            ocena.save()
            flag_already_graded = True
            messages.info(request, 'Promenili ste ocenu vica u ocenu ' + str(grade))
            break
    if not flag_already_graded:
        ocena: Grade = Grade()
        ocena.id_joke = Joke.objects.get(pk=joke_id)
        ocena.id_user = curruser
        ocena.grade = grade
        ocena.date = datetime.datetime.now()
        ocena.save()
        messages.info(request, 'Ocenili ste vic sa ocenom: ' + str(grade))
    try:
        currjoke = Joke.objects.get(pk=joke_id)
        firstBelongsTo = BelongsTo.objects.filter(id_joke=currjoke).first()
        firstcategory = firstBelongsTo.id_category
        return redirect('category', category_id=firstcategory.id_category)    # predji u prikaz iste kategorije
    except:
        return redirect('all_categories')


# vukasin007
@login_required(login_url='login')
def change_personal_data(request: HttpRequest):
    """
    funkcija vraća stranicu sa formama za menjanje podataka i menja podatke ulogovanog korisnika
    :param request:HttpRequest
    :return HttpResponse
    """
    curruser: User = User.objects.get(username=request.user.get_username())
    usernameForm = ChangeUsernameForm(data=request.POST or None)
    if usernameForm.is_valid():
        newUsername = usernameForm.cleaned_data.get('newUsername')
        useri = User.objects.filter(username=newUsername)
        if useri.count() > 0 :
            messages.error(request,"Ovaj username već postoji")

        elif re.search("^[A-Za-z\d]{3,20}$", newUsername):
            curruser.username = newUsername
            curruser.save()
            messages.info(request, "Promenjen username")
        else:
            messages.error(request,"los format")
    firstnameForm = ChangeFirstNameForm(data=request.POST or None)
    if firstnameForm.is_valid():
        newFirstName = firstnameForm.cleaned_data.get('newFirstName')
        if re.search("^[A-Za-z]{2,20}$", newFirstName):
            curruser.first_name = newFirstName
            curruser.save()
            messages.info(request,"promenjen first name")
        else:
            messages.error(request,"Los format")
    lastnameForm = ChangeLastNameForm(data=request.POST or None)
    if lastnameForm.is_valid():
        newLastName = lastnameForm.cleaned_data.get('newLastName')
        if re.search("^[A-Za-z]{2,20}$", newLastName):
            curruser.last_name = newLastName
            curruser.save()
            messages.info(request,"Promenjen last name")
        else:
            messages.error(request,"Los format")
    mailForm = ChangeMailForm(data=request.POST or None)
    if mailForm.is_valid():
        newMail = mailForm.cleaned_data.get('newMail')
        if re.search("^[A-Za-z\d]{2,20}@[A-Za-z\d]{2,20}\.[A-Za-z\d]{2,3}$", newMail):
            curruser.email = newMail
            curruser.save()
            messages.info(request,"Promenjen email")
        else:
            messages.error(request,"Los format")
    passwordForm = ChangePasswordForm(data=request.POST or None)
    if passwordForm.is_valid():
        firstPass = passwordForm.cleaned_data.get('newPassword')
        secondPass = passwordForm.cleaned_data.get('confirm')
        if firstPass != secondPass:
            messages.error(request,"Ne poklapa se potvrda.")
        elif re.search("^.{8,}$", firstPass):    # za sada bez detaljnih provera
            curruser.set_password(firstPass)
            curruser.save()
            messages.info(request,"Promenjen password, bićete izlogovani")
        else:
            messages.error(request,"Nedovoljno jaka sifra")
    context = {
        'usernameForm': usernameForm,
        'firstNameForm': firstnameForm,
        'lastNameForm': lastnameForm,
        'mailForm': mailForm,
        'passwordForm': passwordForm
    }
    return render(request, 'change_data.html', context)


def category_req(request: HttpRequest, category_id):
    """
    funkcija vraća stranicu sa svim vicevima iz kategorije sa identifikatorom category_id
    :param request:HttpRequest, category_id:int
    :return HttpResponse
    """
    belongings = BelongsTo.objects.filter(id_category=category_id)
    category = Category.objects.get(pk=category_id)
    jokes = []
    for belonging in belongings:
        joke = Joke.objects.get(pk=belonging.id_joke.id_joke)
        if joke.status == "A":
            jokes.append(joke)
    context= {
        "jokes" : jokes,
        "category" : category,
    }
    return render(request, 'content.html', context)


def joke(request: HttpRequest, joke_id):
    """
    funkcija vraća stranicu sa sadržajem i komentarima vica sa identifikatorom vica joke_id
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    joke = Joke.objects.get(pk=joke_id)
    comments = Comment.objects.filter(id_joke=joke).filter(status="A")
    autor = User.objects.get(pk=joke.id_user_created.id_user)
    context = {
        "joke" : joke,
        "comments" : comments,
        "autor": autor,
    }
    return render(request, 'single_joke.html', context)


@login_required(login_url='login')
def add_joke(request: HttpRequest):
    """
    funkcija vraća stranicu za dodavanje vica i šalje unet sadržaj na odobravanje
    :param request:HttpRequest
    :return HttpResponse
    """
    if request.method == 'POST':
        title = request.POST['joke_title']
        if (title.__len__() < 1):
            messages.warning(request, "Niste uneli naslov vica")
            return redirect("add_joke")
        content = request.POST['joke_content']
        if (content.__len__() < 1):
            messages.warning(request, "Niste uneli sadrzaj vica")
            return redirect("add_joke")
        new_joke = Joke()
        new_joke.title=title
        new_joke.content=content
        new_joke.id_user_created = request.user
        new_joke.status = "P"
        new_joke.save()
        messages.info(request,"Uspesno ste poslali vic na proveru")
    
    return render(request, "add_joke.html")


@login_required(login_url='login')
def profile(request: HttpRequest):
    """
    funkcija vraća stranicu sa podacima ulogovanog korisnika
    :param request:HttpRequest
    :return HttpResponse
    """
    return render(request, 'profile.html')


@login_required(login_url='login')
def add_comment(request: HttpRequest, joke_id):
    """
    funkcija vraća stranicu za dodavanje komentara na vic sa identifikatorom joke_id i kreira komentar
    :param request:HttpRequest, joke_id:int
    :return HttpResponse
    """
    joke = Joke.objects.get(pk=joke_id)
    context = {
        "joke": joke
    }
    if request.method == "POST":
        content = request.POST["comment_content"]
        if(content.__len__() < 1):
            messages.warning(request,"Niste uneli komentar")
            return redirect("add_comment", joke_id=joke_id)
        new_comment = Comment()
        new_comment.id_joke=joke
        new_comment.id_user = request.user
        new_comment.content = content
        jokes = Comment.objects.filter(id_joke=joke)
        number = jokes.count()+1
        new_comment.ordinal_number = number
        new_comment.status = 'A'
        new_comment.date_posted = datetime.datetime.now()
        new_comment.save()
        messages.info(request, "Uspesno ste dodali komentar")
        return redirect("joke", joke_id=joke.id_joke)

    return render(request, "add_comment.html", context)
