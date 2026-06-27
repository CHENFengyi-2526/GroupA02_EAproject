FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY app app
COPY wsgi.py run.py boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP=run.py \
    PORT=8080 \
    FLASK_ENV=production

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD ["./boot.sh"]
