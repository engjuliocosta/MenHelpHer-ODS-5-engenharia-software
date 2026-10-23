"""Configurações centrais da aplicação (sobrescrevíveis por variáveis de ambiente)."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = os.environ.get("MENHELPHER_HOST", "127.0.0.1")
PORT = int(os.environ.get("MENHELPHER_PORT", "8000"))

DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.environ.get(
    "MENHELPHER_DB", os.path.join(DATABASE_DIR, "menhelpher.db")
)
SCHEMA_SQL = os.path.join(DATABASE_DIR, "schema.sql")
SEED_DOMINIOS_SQL = os.path.join(DATABASE_DIR, "seed_dominios.sql")
SEED_DEMO_SQL = os.path.join(DATABASE_DIR, "seed_demo.sql")

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Limite do corpo das requisições (proteção contra payloads abusivos).
MAX_BODY_BYTES = 16 * 1024
