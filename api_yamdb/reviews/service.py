import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User


def send_email_confirmation(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    user.confirmation_code = confirmation_code
    mail_header = f'Регистрация пользователя завершена успешно!'
    mail_body = f'Ваш код для получения JWT токена {user.confirmation_code}'
    send_mail(mail_header, mail_body, settings.EMAIL_HOST_USER, [user.email])
    user.save()


def check_user_in_base(request):
    if request.data.get('username') and request.data.get('email'):
        username = request.data.get('username')
        email = request.data.get('email')
        return User.objects.filter(
            username=username).filter(email=email).exists()
    return False
