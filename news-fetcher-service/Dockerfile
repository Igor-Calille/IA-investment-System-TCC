# Dockerfile
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000
EXPOSE 5000

# Copia o código da aplicação para o container
COPY . .

# Comando para rodar o aplicativo
CMD ["flask", "--app", "app.webapp.py", "run", "--host=0.0.0.0"]
