FROM python:3.10-slim

# Metadados
LABEL maintainer="matheusferdias@gmail.com"
LABEL description="Sane Aqui - Pesquisa de Saneamento"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (necessárias para MySQL connector)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements primeiro (cache do Docker)
COPY src/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para configurações do Streamlit
RUN mkdir -p /root/.streamlit

# Copiar configurações do Streamlit
COPY src/.streamlit/config.toml /root/.streamlit/config.toml

# Expor porta do Streamlit
EXPOSE 8501

# Healthcheck para verificar se a aplicação está rodando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para executar a aplicação
# Executar aplicação a partir do módulo correto
ENTRYPOINT ["streamlit", "run"]
CMD ["src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
