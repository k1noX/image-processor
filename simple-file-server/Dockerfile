FROM python:3.8-alpine
RUN apk add curl
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5050