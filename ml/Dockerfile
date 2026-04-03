FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["sh", "-c", "uvicorn ml.app:app --host 0.0.0.0 --port ${PORT:-10000}"]