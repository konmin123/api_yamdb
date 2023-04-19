import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from users.models import User


def send_email_confirmation(username):
    """
    Отправляет email с кодом подтверждения пользователю.
    """
    user = get_object_or_404(User, username=username)
    token = default_token_generator.make_token(user)
    mail_header = 'Регистрация пользователя завершена успешно!'
    mail_body = f'Ваш код для получения JWT токена {token}'
    send_mail(mail_header, mail_body, settings.EMAIL_HOST_USER, [user.email])


def check_user_in_base(request):
    """Проверка наличия пользователя в БД."""
    if request.data.get('username') and request.data.get('email'):
        username = request.data.get('username')
        email = request.data.get('email')
        return User.objects.filter(
            username=username).filter(email=email).exists()
    return False
