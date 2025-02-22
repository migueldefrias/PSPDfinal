# Dockerfile
FROM python:3.8-slim

# Instala o Java (necessário para o PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre && \
    rm -rf /var/lib/apt/lists/*

# Define o JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Instala o PySpark e Flask
RUN pip install pyspark flask

# Copia os arquivos da aplicação
COPY app.py /app/app.py
COPY wordcount.py /app/wordcount.py

# Define o diretório de trabalho
WORKDIR /app

# Expõe a porta 5000
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]