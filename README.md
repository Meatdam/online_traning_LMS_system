# Проект Онлайн Обучения Dgango REST framework
________
В мире развивается тренд на онлайн-обучение.<br>
В данном проекте представленна LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.


Данный проект написан не фрейморке Django REST framework, с подключением реляционной базы данных "PostgreSQL"<br>
Ипользовалось вирутальное окружение ```venv```
В  проекте построенно 3 модели БД:
1. Таблица "Users";
2. Таблица "Course";
3. Таблица "Lesson" прямая связь с "Course";

В проекте Описан CRUD для моделей курса и урока.<br> 
Для реализации CRUD для курса (Course) и пользователей (User) использутся Viewsets, а для урока (Lesson) - Generic-классы, <br>
Для запуска проекта необходимо сделать 
1. git clone репозитория
```
git@github.com:Meatdam/online_shop.git
```
2. Установить виртуальное окружение ```venv```
```
python3 -m venv venv
```
3. Подключить виртуальное окружение
```
source venv/bin/activate
```
4. Создать базу данных в ```PgAdmin```, либо через терминал. Необходимо дать название в файле settings.py в каталоге 'config' в константе (словаре) 'DATABASES'
5. Обязательно установить пакет со всеми зависимостями 
```
pip install -r requirements.txt
```
6. Создать файл .env в корне проекта и заполнить следующие данные:
```
# DB settings
ENGINE=
DB_NAME=
USER_DB=
PASSWORD_DB=

# Email settings
EMAIL_HOST_USER_MAIL=
EMAIL_HOST_PASSWORD_MAIL=

# email admin
ADMIN_EMAIL=

# secret key from django
KEY=

# domain settings
DOMAIN=

DEBUG=

# CACHE settings
CACHE_ENABLED=
CACHES_BACKEND=
CACHES_LOCATION=

```

