FROM python:3.11-slim

WORKDIR /app

# 安裝必要套件 + Cloud SQL Proxy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && curl -sSL https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -o /cloud_sql_proxy \
    && chmod +x /cloud_sql_proxy \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# 背景執行 Proxy + Gunicorn（單一指令，減少記憶體壓力）
CMD /cloud_sql_proxy -instances=groupa02eaproject:asia-east1:eadb=tcp:3306 & \
    gunicorn --bind 0.0.0.0:8080 --workers=1 --threads=4 --timeout=180 wsgi:app