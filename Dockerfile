FROM python:3.10

RUN apt update

RUN mkdir "vpn_service"

WORKDIR /vpn_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./poetry.lock ./
COPY ./pyproject.toml ./

RUN python -m pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY ./src ./src
