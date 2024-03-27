FROM python:3.10.10-slim-buster

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .

RUN pytest

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "src.main:app"]