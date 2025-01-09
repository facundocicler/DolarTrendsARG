FROM apache/airflow:2.9.0

# Instalar dependencias necesarias
USER root
RUN apt-get update && apt-get install -y default-jdk && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cambiar al usuario airflow
USER airflow

# Copiar y agregar dependencias de Python
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
