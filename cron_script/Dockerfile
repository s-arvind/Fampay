FROM python:3.9-slim-buster

MAINTAINER Neha Bhardwaj

ENV PYTHONUNBUFFERED=1 \
PYTHONFAULTHANDLER=1 \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=120 \
POETRY_VERSION=1.1.0


WORKDIR /app
COPY . /app

# Install cron
RUN apt-get update && apt-get install -y cron curl build-essential vim \
&& curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
&& . /root/.poetry/env \
&& poetry config virtualenvs.create false \
&& poetry run pip install keyring keyrings.alt \
&& poetry install --no-interaction --no-ansi --no-dev --no-root \
&& apt remove build-essential -y --purge && apt autoremove -y \
&& rm -rf /var/lib/apt/lists/*


RUN chmod +x /app/cron_script/run.sh /app/cron_script/entrypoint.sh

ENTRYPOINT /app/cron_script/entrypoint.sh