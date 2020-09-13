FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python ./manage.py makemigrations
RUN python ./manage.py migrate
CMD python manage.py runserver 127.0.0.1:8000