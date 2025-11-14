FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
# uv 사용 시
RUN pip install uv && uv sync

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
