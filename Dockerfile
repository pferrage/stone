FROM python:3.9-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# workaround to wait for mysql
RUN apt-get update && apt-get install wget build-essential -y
RUN wget http://sourceforge.net/projects/netcat/files/netcat/0.7.1/netcat-0.7.1.tar.gz
RUN tar -xzvf netcat-0.7.1.tar.gz
RUN ./netcat-0.7.1/configure
RUN make
RUN make install
RUN tr -d '\r' < ./wait-for-it.sh > ./wait-for-it-linux.sh
RUN chmod +x wait-for-it-linux.sh

CMD ["./wait-for-it-linux.sh", "mysql:3306", "--", "python", "main.py"]