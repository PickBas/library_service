![Test-CI](https://github.com/2048-IT-Engineers/library_service/workflows/Test-CI/badge.svg)
![Pylint-CI](https://github.com/2048-IT-Engineers/library_service/workflows/Pylint-CI/badge.svg)

![logo](https://github.com/PickBas/library_service/blob/master/assets/fifsmallerlogo.png?raw=true)

# Running project
### 1. Using [Docker](https://www.docker.com/)
Open terminal in the project directory, enter the following command:

      docker-compose up --build
    
Now the app is available on *127.0.0.1:8000*
### 2. Using [Python](https://www.python.org/)

      python -m venv ./venv
      ./venv/bin/activate or .\venv\Scripts\activate for win
      python -m pip install -U pip
      python -m pip install -r requirements.txt
      python manage.py makemigrations
      python manage.py migrate
      python manage.py loaddata fixtures/site_fixtures.json
      python manage.py runserver   

Now the app is available on *127.0.0.1:8000*
