# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código fonte da aplicação e o script wait-for-it
COPY src/ .

# Conceda permissão de execução para o script wait-for-it
RUN chmod +x wait-for-it.sh

# Comando para rodar o programa Python, aguardando o MySQL estar pronto
CMD ["./wait-for-it.sh", "mysql:3306", "--", "python", "main.py"]
