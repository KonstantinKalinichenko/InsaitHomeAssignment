FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./App /app


EXPOSE 8000
CMD ["waitress-serve", "--port=8000", "app:app"]