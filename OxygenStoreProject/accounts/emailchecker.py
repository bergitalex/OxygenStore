import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_confirmation_code(length=6):
    """Генерирует случайный код подтверждения."""
    return ''.join(random.choices(string.digits, k=length))

def send_confirmation_email(email, code):
    """Отправляет код подтверждения на указанный email."""
    subject = 'Код подтверждения для изменения Email'
    message = f'Ваш код подтверждения: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email], fail_silently=False)
