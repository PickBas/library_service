![Test-CI](https://github.com/2048-IT-Engineers/library_service/workflows/Test-CI/badge.svg)
![Pylint-CI](https://github.com/2048-IT-Engineers/library_service/workflows/Pylint-CI/badge.svg)

![logo](https://github.com/PickBas/library_service/blob/master/assets/fifsmallerlogo.png?raw=true)

# Запуск проекта
### 1. Используя [Docker](https://www.docker.com/)
Откройте командную строку в папке с проектом, далее введите команду:

      docker-compose up --build
    
Теперь вы можете открыть сайт в браузере, введя *127.0.0.1:8000*
### 2. Вручную, используя [Python](https://www.python.org/)
* Перейдите на [сайт](https://www.python.org/), скачайте последнюю версию Python и установите его. Во время установки **обязательно** выберете пункт *Add Python 3.8 to PATH*
* Откройте командную строку в папке проекта, введите команды:

      python -m pip install -U pip
      python -m venv .\venv
      venv\Scripts\activate
      python -m pip install -U pip
      python -m pip install -r requirements.txt
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver
      
Теперь вы можете открыть сайт в браузере, введя *127.0.0.1:8000*

## Git
* [Установка Git](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/GIT_INSTALLATION.md)
* [Туториал по Git](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/GIT_TUTORIAL.md)
