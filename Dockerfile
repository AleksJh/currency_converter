FROM python:3.13-slim

ENV POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION && \
    apt-get purge -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --only main

COPY . .

CMD ["poetry", "run", "python", "./src/currency_app/main.py"]
