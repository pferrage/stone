FROM python:3.9.12

WORKDIR /app

RUN mkdir /app/src/
COPY src/ /app/src

RUN pip install --no-cache-dir -r src/requirements.txt

ENV PYTHONPATH=/app/src

# Comando para rodar o programa
CMD ["python", "src/main.py"]
