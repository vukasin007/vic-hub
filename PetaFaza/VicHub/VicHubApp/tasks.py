# independent file

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User
# vukasin007

# @periodic_task(
#     run_every=(crontab(hour=12, minute=00, day_of_week=6)),
#     name="Dispatch_scheduled_mail",
#     reject_on_worker_lost=True,
#     ignore_result=True)
# def schedule_mail():
#     message = render_to_string('template/bilten_email_template.html')
#     mail_subject = 'Bilten nedeljni mejl'
#     toWhom = User.objects.filter(subscribed__equals="Y")
#     for to_email in toWhom:
#         email = EmailMessage(mail_subject, message, to=[to_email])
#         email.send()
