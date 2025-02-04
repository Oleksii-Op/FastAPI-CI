ARG PYTHON_VERSION=3.12.7

FROM python:${PYTHON_VERSION}-slim

LABEL description="FastAPI CI"

ENV POETRY_VERSION=1.8.3

ENV POETRY_CACHE_DIR=/app/.cache

RUN apt-get update -y \
    && apt install wget -y \
    && pip install poetry==${POETRY_VERSION}

WORKDIR /app/

COPY . .

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main \
    && useradd --shell /bin/bash backend \
    && chown -R backend:backend /app

USER backend

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]
