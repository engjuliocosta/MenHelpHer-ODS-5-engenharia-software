"""Utilitários compartilhados pelos testes (banco temporário isolado)."""

import os
import shutil
import tempfile
import unittest

from backend.database import Database


class BancoTemporarioTestCase(unittest.TestCase):
    """Cada teste roda em um arquivo SQLite novo, com catálogos e demo carregados."""

    carregar_demo = True

    def setUp(self):
        self._pasta = tempfile.mkdtemp(prefix="menhelpher_test_")
        self.db = Database(os.path.join(self._pasta, "teste.db"))
        self.db.inicializar(carregar_demo=self.carregar_demo)
        self.addCleanup(shutil.rmtree, self._pasta, ignore_errors=True)


PAYLOAD_COMPROMISSO = {
    "nome": "Ada Teste",
    "papel": "Estudante de Engenharia de Software",
    "tipo": "Mentoria Ativa",
    "mensagem": "Vou mentorar colegas iniciantes de forma contínua.",
}

PAYLOAD_AVALIACAO = {
    "perfil": "Estudante",
    "clareza": 5,
    "aprendizado_vieses": 4,
    "relevancia_ods5": 5,
    "comentario": "Ótima plataforma.",
}
