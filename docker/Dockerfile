FROM python:3.9.12

WORKDIR /app

RUN mkdir /app/files
RUN mkdir /app/files/csv
RUN mkdir /app/sqlite3

RUN mkdir /app/src/tools
RUN mkdir /app/src/bronze
RUN mkdir /app/src/silver
RUN mkdir /app/src/gold
RUN mkdir /app/src/quality


COPY requirements.txt /app/
COPY main.py /app/
COPY __init__.py /app/

COPY files/*.zip /opt/files/
COPY files/csv/*.csv /opt/files/csv

COPY sqlite3/*.db /app/sqlite3

COPY tools/*.py /app/src/tools
COPY bronze/*.py /app/src/bronze
COPY silver/*.py /app/src/silver
COPY gold/*.py /app/src/gold
COPY quality/*.py /app/src/quality


RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o programa
CMD ["python", "__init__.py"]