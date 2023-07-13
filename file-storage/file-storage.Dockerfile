FROM python:3.9-alpine
RUN apk add curl
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
WORKDIR /src
ADD ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
ADD src /src