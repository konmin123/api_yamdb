# api_yamdb

## **Описание проекта YaMDb:**
Проекта YaMDb, собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр (были предустановлены). 
Добавлять произведения, категории и жанры может только администратор.
Читатели оставляют к произведениям текстовые отзывы, и выставляют произведению оценку 
(в диапазоне от одного до десяти). Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
На одно произведение пользователь может оставить только один отзыв!
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
Аутентификация пользователей происходит по JWT-токену.

## Как запустить проект:

**Клонировать репозиторий с GitHub и перейти в него в командной строке:**

```
git clone git@github.com:konmin123/api_yamdb.git
```

**Установить виртуальное окружение venv:**
```
python -m venv venv
```

**Aктивировать виртуальное окружение venv:**
```
source venv/Scripts/activate
```

**Обновить менеджер пакетов pip:**
```
python -m pip install --upgrade pip
```

**Установить зависимости из файла requirements.txt:**
```
pip install -r requirements.txt
```
**Cоздать скрипт миграций:**
```
python manage.py makemigrations
```

**Выполнить миграции:**
```
python manage.py migrate
```

**Создать суперпользователя:**
```
python manage.py createsuperuser
```

**Запустить проект:**
```
python manage.py runserver
```

## **Примеры запросов API:**

***Регистрация пользователя:***
```
POST /api/v1/auth/signup/
```
тело запроса: <br>
{"username": "some_username","email": "email@yandex.ru"} <br>
ответ: <br>
{"username": "some_username","email": "email@yandex.ru"} <br>

***Получение JWT токена:***
```
POST api/v1/auth/token/
```
тело запроса: <br>
{"username": "some_username", "confirmation_code": "bmz33w-324ec1a6a945b7e49158347f4ebee896"} <br>

ответ: <br>
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMDk5NDczLCJpYXQiOjE2ODIwMTMwNzMsImp0aSI6ImVkOTIxNTg3ZGU0NDQwYjRhMDdjNDg2OGY4ZTg5N2NjIiwidXNlcl9pZCI6Mn0._kSa_1V3pzbfWhNEjklEpcpH1xYu8r1d2EiBUpksc94"} <br>

***Получение данных своей учетной записи:***
```
GET /api/v1/users/me/
```
тело запроса: <br>
пустое <br>

ответ: <br>
{"username":"some_username","email":"email@yandex.ru","first_name":"","last_name":"","bio":"","role":"user"}<br>


## Документация к проекту:

***Документация для API после установки доступна по адресам:***
```
http://127.0.0.1:8000/redoc/
http://127.0.0.1:8000/docs/
```

## Технологии:
+ Python 3.9
+ Django 3.2
+ Django Rest Framework 3.12.4
+ SQLite3
+ Postman
+ Swagger