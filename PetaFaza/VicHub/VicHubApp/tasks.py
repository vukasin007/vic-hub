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
        print("1\n")
        # ocene = Grade.objects.filter(date__gt=(datetime.datetime.now() - datetime.timedelta(days=7))) ne razumem zasto ne radi
        ocene = Grade.objects.filter(was_reviewed='N')
        print("1\n")
        for oc in ocene:
            print(oc+"\n")
        adekvatne_ocene = []
        print("2\n")
        for ocena in ocene:
            ocena.was_reviewed = "Y"
            ocena.save()
            if ocena.id_joke.status == "B":
                adekvatne_ocene.append(ocena)
        print("3\n")
        num_ocena = dict()  # key: id vica, value: broj ocena
        sum_ocena = dict()  # slicno
        for ocena in adekvatne_ocene:
            id_vica = ocena.id_joke
            num = num_ocena.get(id_vica, 0)
            num_ocena[id_vica] = num + 1
            suma = sum_ocena.get(id_vica, 0)
            sum_ocena[id_vica] = suma + 1
        print("4\n")
        avg_dict = dict()
        max = -1
        target_joke = -1
        for key in num_ocena:
            avg_dict[key] = sum_ocena[key] / num_ocena[key]
            if max < avg_dict[key]:
                max = avg_dict[key]
                target_joke = key
        print("5\n")
        if target_joke == -1:
            raise Exception("nepar")
        mail_message = Joke.objects.get(target_joke).title + "\n" + Joke.objects.get(target_joke).content
        print("6\n")
    except:
        mail_message = "Kako se zove vepar sa tri noge?\n\n\tVepar\n\t\t\t-admini"

    # for to_email in all_subscribed:
    #     mail_message = f'Zdravo {to_email.username}, ovo nedeljni vic je:\n' + mail_message
    #     recipient_list = [to_email.email]
    #     send_mail(mail_subject, mail_message, email_from, recipient_list)
    #     print("sent email to " + to_email.username)
    return "Email sending finished ok"
