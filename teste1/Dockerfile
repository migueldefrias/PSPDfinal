# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar o código da aplicação
COPY wordcount.py .
COPY input.txt .
COPY input2.txt .
COPY input3.txt .
COPY input4.txt .
COPY input5.txt .
COPY input6.txt .
COPY input7.txt .
COPY input8.txt .
COPY input9.txt .
COPY input10.txt .

# Comando padrão para executar a aplicação
CMD ["sh", "-c", "python wordcount.py && tail -f /dev/null"]

