# 1. Imagem Base
# Começamos com uma imagem oficial do Python 3.11 (slim é menor)
FROM python:3.11-slim

# 2. Diretório de Trabalho
# Define onde o código ficará dentro do container
WORKDIR /app

# 3. Instalação de Dependências
# Copia só o 'requirements.txt' primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar Código da Aplicação
# Copia o resto do seu projeto para dentro do container
COPY . .

# 5. Expor a Porta
# Informa ao Docker que o Uvicorn rodará na porta 8000
EXPOSE 8000

# 6. Comando de Execução
# O comando para iniciar a API
# Usamos 0.0.0.0 para aceitar conexões de fora do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]