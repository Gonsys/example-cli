FROM python:3.14-alpine

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Criar diretório de trabalho
WORKDIR /app

# Copiar pyproject.toml e instalar dependências
COPY pyproject.toml .
RUN uv pip install --system .

# Copiar código da aplicação
COPY app/ ./app/

# Expor porta
EXPOSE 8000

# Comando de entrada
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
