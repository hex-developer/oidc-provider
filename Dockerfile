FROM python:alpine

RUN apk add --no-cache git

RUN pip install --upgrade pip setuptools gunicorn

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk del git

COPY ./ ./

EXPOSE 8000
CMD /app/entrypoint.sh
