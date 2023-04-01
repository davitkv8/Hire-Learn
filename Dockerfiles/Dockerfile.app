FROM python:3.10

# needed for postgre lib
RUN apt update && apt -y install libpq-dev gcc

ADD requirements/requirements.app.txt .

RUN pip install -r requirements.app.txt

ADD . /app/

RUN chmod 777 /app

WORKDIR /app/

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
