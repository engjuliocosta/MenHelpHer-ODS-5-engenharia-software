# ==============================================================================
# MenHelpHer / EquiTech ODS 5 - Dockerfile de Produção e Testes
# Projeto Integrado Transdisciplinar (PIT I e PIT II) - Engenharia de Software
# Instituição: Universidade Cruzeiro do Sul
# Autor: Julio Costa
# ==============================================================================

FROM python:3.12-slim

# Evita geração de bytecode .pyc e força flush imediato dos logs stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MENHELPHER_HOST=0.0.0.0 \
    MENHELPHER_PORT=8000 \
    MENHELPHER_DB=/app/database/menhelpher.db

WORKDIR /app

# Instalação de utilitários mínimos do sistema (curl para o HEALTHCHECK)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Instalação de dependências Python para execução da aplicação e suíte de testes
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Cópia integral do código-fonte, banco de dados e front-end
COPY . /app/

# Criação de usuário não-privilegiado para segurança do contêiner
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/database && \
    chown -R appuser:appuser /app

USER appuser

# Exposição da porta de comunicação HTTP
EXPOSE 8000

# Verificação periódica de saúde (Healthcheck do contêiner)
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/saude || exit 1

# Ponto de entrada padrão: Servidor HTTP nativo com arquitetura MVC
CMD ["python3", "server.py"]
