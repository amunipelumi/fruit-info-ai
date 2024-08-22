from django.core.mail import send_mail
from celery import shared_task
import time
import os



SUBJECT = 'Fruit-Info AI' 
MESSAGE = 'This is our first ever mail to you.\nHope this message finds you well' 
SOURCE = os.getenv('SOURCE_EMAIL')
DESTINATION = os.getenv('DEST_EMAIL').split(',')


# @shared_task
# def sleepfunc(timer):
#     time.sleep(timer)
#     return None


@shared_task
def email_task():
    time.sleep(15)
    send_mail(
        subject=SUBJECT,
        message=MESSAGE,
        from_email=SOURCE,
        recipient_list=DESTINATION
    )
    return None