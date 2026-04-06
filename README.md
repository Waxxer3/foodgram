# Yatube API

Учебный REST API для работы с постами, комментариями и подписками.  
Позволяет: создавать посты, оставлять комментарии, подписываться на пользователей и получать свои подписки.

---

## Postman-коллекция для проверки API

Файл `postman_collection/API_for_yatube.postman_collection.json` содержит коллекцию запросов для проверки работы API.

---

## Подготовка Django-проекта к запуску коллекции

1. Проверьте, что виртуальное окружение развернуто и активировано, зависимости проекта установлены.
2. Перейдите в директорию проекта создайте и активируйте виртуальное окружение, а также выполните миграции:

```bash
python -m venv venv
source venv/bin/activate
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Выполните миграции:
```bash
python manage.py migrate
```
## Аутентификация
```bash
POST /api/v1/jwt/create/
{
    "username": "ваш_логин",
    "password": "ваш_пароль"
}
```

## Запуск Docker-контейнеров
Убедитесь, что у вас установлен Docker и Docker Compose. Находясь в папке infra/, запустите сборку:

```bash
docker-compose up -d --build
```

## Настройка базы данных и статики
После успешного запуска выполните серию команд внутри контейнера backend:
# Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
# Соберите статику (админка и API):

```bash
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend cp -r /app/static_backend/. /app/static/
```
# Создайте суперпользователя (Администратора):

```bash
docker-compose exec backend python manage.py createsuperuser
```
# Наполнение данными
Чтобы не добавлять сотни ингредиентов вручную, воспользуйтесь командой импорта:
```bash
docker-compose exec backend python manage.py load_ingredients
```