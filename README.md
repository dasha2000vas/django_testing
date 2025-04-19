# Django testing  
## Pytest и unit тесты для проектов ya_news и ya_note.
```
django_testing
├── ya_news
│   ├── news
│   │   ├── fixtures/
│   │   ├── migrations/
│   │   ├── pytest_tests/   <- pytest тесты для проекта ya_news
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates/
│   ├── yanews/
│   ├── manage.py
│   └── pytest.ini
├── ya_note
│   ├── notes
│   │   ├── migrations/
│   │   ├── tests/          <- unittest тесты для проекта ya_note
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates/
│   ├── yanote/
│   ├── manage.py
│   └── pytest.ini
├── .gitignore
├── README.md
├── requirements.txt
└── structure_test.py
```

## Как скачать и запустить проект:

**1. Клонировать в нужную папку**
```
git clone git@github.com:dasha2000vas/django_testing.git
```

**2. Создать и активировать виртуальное окружение**
```
python -m venv venv
```
```
source venv/Scripts/activate
```

**3. Установить зависимости из файла requirements.txt**
```
pip install -r requirements.txt
```

**4. Запустить скрипт для `run_tests.sh` из корневой директории проекта:**
```sh
bash run_tests.sh
```

## Технический стек:
* django3.2.15
* pytest7.1.3

## Автор:
* Василевская Дарья
* GitHub: https://github.com/dasha2000vas
* Телеграм: https://t.me/vasdascha
* Почта: vasilevsckaya.dascha@yandex.ru
