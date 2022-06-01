# independent file
import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import *
from django.core.mail import send_mail
# vukasin007
from VicHub.settings import EMAIL_HOST_USER


@shared_task(name="tick")
def tick():
    print("tick")
    return "return from tick: radi ok"


@shared_task(name="send-mail-function")
def schedule_mail():
    mail_subject = 'Bilten mejl'
    all_subscribed = User.objects.filter(subscribed__exact="Y")
    email_from = EMAIL_HOST_USER
    # pronadji najbolji vic
    try:
        ocene = Grade.objects.all()
        adekvatne_ocene = []
        for ocena in ocene:
            # ocena.was_reviewed = "Y"
            ocena.save()
            if ocena.id_joke.status == "A":
                adekvatne_ocene.append(ocena)
        num_ocena = dict()  # key: id vica, value: broj ocena
        sum_ocena = dict()  # slicno
        for ocena in adekvatne_ocene:
            id_vica = ocena.id_joke.id_joke
            num = num_ocena.get(id_vica, 0)
            num_ocena[id_vica] = num + 1
            suma = sum_ocena.get(id_vica, 0)
            sum_ocena[id_vica] = suma + ocena.grade
        max = -1
        target_joke = -1
        for key in num_ocena:
            if max < (sum_ocena[key] / num_ocena[key]):
                max = sum_ocena[key] / num_ocena[key]
                target_joke = key
        if max == -1:
            print("exception\n")
            raise Exception("nepar")
        print(target_joke)
        mail_message = Joke.objects.get(pk=target_joke).title + "\n\n-" + Joke.objects.get(pk=target_joke).content
        myjoke = Joke.objects.get(pk=target_joke)
        myjoke.status = "B"
        myjoke.save()
        print(mail_message)
    except:
        mail_message = "Vepar\n\nKako se zove vepar sa tri noge?\n-Vepar"

    for to_email in all_subscribed:
        message = f'Zdravo {to_email.username}, ovonedeljni vic je:\n\n {mail_message}'
        recipient_list = [to_email.email]
        send_mail(mail_subject, message, email_from, recipient_list)
        print("sent email to " + to_email.username)
    return "Email sending finished ok"
