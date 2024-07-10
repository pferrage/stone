FROM python:3.9.12

WORKDIR /app

RUN mkdir /app/src/
COPY src/* /app/src

RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o programa
CMD ["python", "main.py"]
