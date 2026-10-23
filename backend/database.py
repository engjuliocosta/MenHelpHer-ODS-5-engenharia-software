"""Camada de acesso ao banco de dados (SQLite 3 - módulo padrão ``sqlite3``)."""

import os
import sqlite3
from contextlib import contextmanager

from . import config


class Database:
    """Cria conexões por operação (seguro para o servidor multithread)."""

    def __init__(self, caminho=None):
        self.caminho = caminho or config.DATABASE_PATH

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.caminho, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _ler(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()

    def inicializar(self, carregar_demo=True):
        """Cria o esquema, os catálogos e (em banco novo) os dados de demonstração."""
        pasta = os.path.dirname(self.caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with self.connection() as conn:
            conn.executescript(self._ler(config.SCHEMA_SQL))
            conn.executescript(self._ler(config.SEED_DOMINIOS_SQL))
            if carregar_demo:
                vazio = (
                    conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0] == 0
                    and conn.execute("SELECT COUNT(*) FROM avaliacao").fetchone()[0] == 0
                )
                if vazio:
                    conn.executescript(self._ler(config.SEED_DEMO_SQL))
