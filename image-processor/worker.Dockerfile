FROM python:3.9-alpine
ADD ./requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install -r requirements.txt
ADD src /src
ENV PYTHONUNBUFFERED=1 