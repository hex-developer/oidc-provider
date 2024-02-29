FROM python:alpine

RUN pip install --upgrade pip setuptools gunicorn

RUN mkdir /app
WORKDIR /app

COPY ./ ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["/app/entrypoint.sh"]
