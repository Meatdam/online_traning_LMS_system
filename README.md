# Проект Онлайн Обучения (Django REST framework)
________
В мире развивается тренд на онлайн-обучение.<br>
В данном проекте представленна LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.


Данный проект написан не фрейморке Django REST framework, с подключением реляционной базы данных "PostgreSQL"<br>
Ипользовалось вирутальное окружение ```venv```
В  проекте построенно 3 модели БД:
1. Таблица "Users";
2. Таблица "Course";
3. Таблица "Lesson" прямая связь с "Course";
4. Таблица "Payments" прямая связь с "Course", "Lesson", "User";

В проекте Описан CRUD для моделей курса и урока.<br> 
Для реализации CRUD для курса (Course) и пользователей (User) использутся Viewsets, а для урока (Lesson) - Generic-классы, <br>
Для работы с приложением использовалась программа "Postman"<br>
Для запуска проекта без использования Docker необходимо сделать 
1. git clone репозитория
```
git@github.com:Meatdam/online_traning_LMS_system.git
```
2. Установить виртуальное окружение `venv`
```
python3 -m venv venv для MacOS и Linux систем
python -m venv venv для windows
```
3. Активировать виртуальное окружение
```
source venv/bin/activate для MasOs и Linux систем
venv\Scripts\activate.bat для windows
```
4. установить файл с зависимостями
```
pip install -r requirements.txt
```
4. Создать базу данных в ```PgAdmin```, либо через терминал. Необходимо дать название в файле settings.py в каталоге 'base' в константе (словаре) 'DATABASES'

5. Создать файл .env в корне проекта и заполнить следующие данные:
```
SECRET_KEY=

DEBUG=

# DB settings
POSGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

ADMIN_EMAIL=

```
Запуск приложения через Docker:<br>
1. Повторить шаги 1-3
2. Запустить Docker локально на машине
3. Выполнить команду в терминале
```
docker compose up -d --build
```
Данная команда сразу создаст образ, и сбилдит его, т.е. запустит локально в Docker
4. Переходим по ссылке ```http://localhost:8000/```
Чтобы удалить контейнеры после работы с приложением используйте команду 
```
docker-compose down 
```

Автор проекта:<br>
[Кузькин Илья](https://github.com/Meatdam)

