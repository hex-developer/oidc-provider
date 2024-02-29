FROM python:alpine

RUN pip install --upgrade pip setuptools gunicorn

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000
CMD ["/app/entrypoint.sh"]
