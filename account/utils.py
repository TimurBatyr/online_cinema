from django.core.mail import send_mail
from online_cinema._celery import app

@app.task
def send_activation_code(email, activation_code):

    message = f"""Thanks for registration.Please activate your account:
    http://127.0.0.1:8000/api/v1/account/activation/{activation_code}"""
    send_mail(
        'Account activation',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )
