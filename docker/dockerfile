FROM python:3.11

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . /app

ENV ENV=production

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
  