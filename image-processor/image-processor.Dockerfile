FROM python:3.9-alpine
RUN apk add curl
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
ADD ./image-processor-requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install -r requirements.txt
ADD src /src