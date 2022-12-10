FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install curl -y

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./app /app

COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml

RUN poetry install

WORKDIR /app
