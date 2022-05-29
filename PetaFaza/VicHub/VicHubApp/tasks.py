# independent file
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User
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

    for to_email in all_subscribed:
        mail_message = f'Zdravo {to_email.username}, ovo je test mejl'
        # email = EmailMessage(mail_subject, mail_message, to=[to_email])
        # email.send()
        recipient_list = [to_email.email]
        send_mail(mail_subject, mail_message, email_from, recipient_list)
        print("sent email to " + to_email.username)
    return "Email sending finished ok"
