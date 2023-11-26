from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_result(name, total, score, percent, correct, wrong, created_at, email):
    send_mail(
        subject='Your Results',
        message=f'''
            Name: {name}
            Total questions: {total}
            Your Score: {score}
            Percent: {percent}%
            Number of correct Questions: {correct}
            Number of wrong Questions: {wrong}
            Date: {created_at.date()}
        ''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
