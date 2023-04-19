from api.v1.service import actual_year

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Функция validate_year проверяет, является ли переданный год (value)
    больше текущего года (actual_year). Если переданный год больше
    текущего года, то функция выбрасывает исключение ValidationError.
    """
    if value > actual_year():
        raise ValidationError('Будущее еще не наступило')
