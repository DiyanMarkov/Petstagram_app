FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

#COPY . /app/
COPY manage.py /app/manage.py
COPY mediafiles /app/mediafiles
COPY core /app/core
COPY templates /app/templates
COPY petstagram /app/petstagram
COPY staticfiles /app/staticfiles

