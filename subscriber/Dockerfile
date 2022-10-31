FROM python:3.9-slim-buster

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY app.py /app/app.py
