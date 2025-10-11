FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential libpq-dev netcat-openbsd  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app
RUN chmod +x /app/entrypoint.sh
