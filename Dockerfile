FROM python:stretch

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apt update
RUN apt install python3-pip -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn","-b",":8080","api:app" ]
