FROM python:3.9-slim-buster

LABEL vendor="fampay"

ENV PYTHONUNBUFFERED=1 \
PYTHONFAULTHANDLER=1 \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=120 \
POETRY_VERSION=1.1.0


WORKDIR /app
COPY . /app

RUN apt-get update \
&& apt-get install curl build-essential vim -y \
&& curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
&& . /root/.poetry/env \
&& poetry config virtualenvs.create false \
&& poetry run pip install keyring keyrings.alt \
&& poetry install --no-interaction --no-ansi --no-dev --no-root \
&& apt remove build-essential -y --purge && apt autoremove -y \
&& rm -rf /var/lib/apt/lists/*

CMD ["sh", "/app/run-app.sh"]