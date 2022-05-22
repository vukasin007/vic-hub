# independent file
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User
# vukasin007


@shared_task(name="tick")
def tick():
    print("tick")
    return "return from tick: radi ok"


@shared_task(name="send mail function")
def schedule_mail():
    message = render_to_string('bilten_email_template.html')
    mail_subject = 'Bilten nedeljni mejl'
    all_subscribed = User.objects.filter(subscribed__equals="Y")
    for to_email in all_subscribed:
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
