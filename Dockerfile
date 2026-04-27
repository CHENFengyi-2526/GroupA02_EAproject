FROM python:3.11-slim

#deploy docker

# FROM python:3.11-slim

# RUN useradd -m -s /bin/bash appuser

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt gunicorn

# COPY app app
# COPY app/config.py run.py boot.sh ./

# RUN chmod +x boot.sh

# ENV FLASK_APP run.py
# RUN chown -R appuser:appuser /app
# USER appuser

# EXPOSE 8080
# CMD ["./boot.sh"]




#deploy GCP(Cloud run)

#WORKDIR /app

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    gcc libpq-dev curl \
#    && curl -sSL https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -o /cloud_sql_proxy \
#    && chmod +x /cloud_sql_proxy \
#    && rm -rf /var/lib/apt/lists/*

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#ENV PYTHONUNBUFFERED=1 \
 #  PORT=8080

#CMD /cloud_sql_proxy -instances=groupa02eaproject:asia-east1:eadb=tcp:3306 & \
#    gunicorn --bind 0.0.0.0:8080 --workers=1 --threads=4 --timeout=180 wsgi:app

#deploy GCP(GKE)
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