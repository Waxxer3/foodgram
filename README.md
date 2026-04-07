# Foodgram — Продуктовый помощник

Foodgram — это веб-приложение, где пользователи могут публиковать рецепты, добавлять их в избранное, формировать список покупок и скачивать его.


## Описание

Проект реализует REST API и фронтенд для сервиса публикации рецептов.

Пользователи могут:

* создавать рецепты
* добавлять рецепты в избранное
* добавлять рецепты в список покупок
* скачивать список покупок
* подписываться на авторов


## Технологии

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL
* Docker / Docker Compose
* Nginx
* Gunicorn


## Как развернуть проект

### 1. Клонировать репозиторий

```bash
git clone <ссылка_на_репозиторий>
cd foodgram
```


### 2. Создать .env файл

Пример:

```env
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```


### 3. Запустить контейнеры

Перейдите в папку infra:

```bash
cd infra
docker-compose up -d --build
```


### 4. Выполнить миграции и собрать статику

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```


### 5. Создать суперпользователя

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Заполнить ингредиенты

```bash
docker-compose exec backend python manage.py load_ingredients
```

## Доступ к проекту

* Сайт: http://foodgramyandexprac.duckdns.org
* API: http://foodgramyandexprac.duckdns.org/api/
* Админка: http://foodgramyandexprac.duckdns.org/admin/


## Данные для входа в админку

* Логин: Admin
* Пароль: 57193

## Автор

* Waxxer3
