FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python ./manage.py makemigrations
RUN python ./manage.py migrate
RUN python ./manage.py loaddata ./fixtures/site_fixtures.json