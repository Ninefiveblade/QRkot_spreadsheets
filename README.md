# QRkot_spreadseets

Благотворительный проект котиков, создает проекты для инвестиций, принмает пожертвования
Делает котиков лучше, с возможностью вывода сводки таблиц о закрытых проектов, по их скорости закрытия.

# Технологии:
fastapi-users-db-sqlalchemy==4.0.3
fastapi-users[sqlalchemy]==10.0.4
fastapi==0.78.0
uvicorn[standard]==0.17.6
pydantic==1.9.1
aiosqlite==0.17.0
google-auth==2.8.0
aiogoogle==4.2.0

# Установка проекта
## Клонируйте репозиторий на локальный компьютер:
```git@github.com:Ninefiveblade/cat_charity_fund.git```
## Перейдите в папку проекта:
```cd cat_charity_fund```

# Подготовка к запуску проекта:
Необходимо установить виртуальное окружение:
```python3.9 -m pip install --upgrade pip```
Установить зависимости:
```source venv/bin/activate```
```(venv) $ pip install -r requirements```

# Формирование таблицы
Сделайте POST запрос на эндпоинт /google


# Применение существующих миграций:

``` alembic upgrade head ```

# Запуск проекта:
Выполните из корневой директории
``` (venv) uvicorn app.main:app --reload ```

# ссылка на документацию доступно по адресу
``` http://localhost/redoc ```
``` http://localhost/docs ```

# Лицензия:
[LICENSE MIT](LICENSE)

# Aвтор:
[Алексеев Иван](https://github.com/Ninefiveblade)
