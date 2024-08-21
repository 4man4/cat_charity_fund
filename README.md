# QRKot

## Описание:
Благотворительный фонд помощи котикам

### Технологии:
- Python 3.9
- FastAPI 0.78

## Работа с сервисом:

#### Клонировать репозиторий и перейти в него в командной строке:
```shell
git clone git@github.com:4man4/cat_charity_fund.git
```
```shell
cd cat_charity_fund
```

#### Cоздать и активировать виртуальное окружение:
```shell
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```shell
    source venv/bin/activate
    ```
* Если у вас windows
    ```shell
    source venv/scripts/activate
    ```

#### Установить зависимости из файла requirements.txt:
```shell
python3 -m pip install --upgrade pip
```
```shell
pip install -r requirements.txt
```

#### В корневой директории проекта создать файл `.env` и внести следующие переменные:
__APP_TITLE__ - Название приложения. По умолчанию `QRKot`.<br>
__APP_DESCRIPTION__ - Описание приложения. По умолчанию `Благотворительный фонд помощи котикам`.<br>
__APP_VERSION__ - Версия приложения. По умолчанию `1.0.0`.<br>
__DATABASE_URL__ - Драйвер БД и путь к ней. По умолчанию `sqlite+aiosqlite:///./fastapi.db`.<br>
__SECRET__ - Секретный ключ проекта.<br>
__FIRST_SUPERUSER_EMAIL__ - Логин администратора.<br>
__FIRST_SUPERUSER_PASSWORD__ - Пароль администратора.<br>

## Автор
**Петр Горюнов**  
[Профиль GitHub](https://github.com/4man4)
