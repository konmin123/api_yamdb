import datetime as dt
from django.conf import settings
from django.core.mail import send_mail


def send_email_confirmation(user, confirmation_code):
    """Отправка кода подтверждения по email."""
    mail_header = 'Регистрация пользователя завершена успешно!'
    mail_body = f'Ваш код для получения JWT токена {confirmation_code}'
    send_mail(mail_header, mail_body, settings.EMAIL_HOST_USER, [user.email])


def actual_year():
    """
    Функция actual_year возвращает текущий год в формате int.
    """
    return dt.datetime.now().year
