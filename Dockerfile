#usar uma imagem alpine para reduzir o tamanho da imagem
FROM python:3.10-alpine

# Instalação de dependências usando o apk do alpine
RUN apk update && \
    apk add bash nano postgresql-dev gcc python3-dev musl-dev

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os requisitos e instalando
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código fonte
COPY . .

# Comando padrão a ser executado quando o contêiner for iniciado
# comando de migração, aguarda o banco de dados estar pronto para rodar
# CMD bash -c "while ! nc -z db_postgres 5432; do sleep 1; done && alembic upgrade head && python app.py"
CMD bash -c "python app.py"
# Expondo a porta 8000
EXPOSE 8000