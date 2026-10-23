"""Testes unitários isolados para a camada de acesso a dados backend/database.py."""

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from backend import config
from backend.database import Database


class DatabaseUnitTest(unittest.TestCase):
    """Testa a classe Database, conexões, contexto transacional e inicialização."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_unit.db")
        self.db = Database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_instanciacao_com_caminho_customizado_e_padrao(self):
        db_custom = Database("/tmp/minha_base.db")
        self.assertEqual(db_custom.caminho, "/tmp/minha_base.db")

        db_padrao = Database()
        self.assertEqual(db_padrao.caminho, config.DATABASE_PATH)

    def test_ler_arquivo_sql_valido(self):
        conteudo = Database._ler(config.SCHEMA_SQL)
        self.assertIn("CREATE TABLE IF NOT EXISTS", conteudo)

    def test_ler_arquivo_inexistente_lanca_excecao(self):
        with self.assertRaises(FileNotFoundError):
            Database._ler(os.path.join(self.temp_dir.name, "inexistente.sql"))

    def test_connection_context_manager_commit_e_fechamento(self):
        with self.db.connection() as conn:
            conn.execute("CREATE TABLE teste (id INTEGER PRIMARY KEY, valor TEXT)")
            conn.execute("INSERT INTO teste (valor) VALUES ('teste1')")
            # Valida row_factory configurado
            res = conn.execute("SELECT valor FROM teste WHERE id=1").fetchone()
            self.assertIsInstance(res, sqlite3.Row)
            self.assertEqual(res["valor"], "teste1")

        # Conexão subsequente comprova que o commit persistiu
        with self.db.connection() as conn2:
            res2 = conn2.execute("SELECT valor FROM teste WHERE id=1").fetchone()
            self.assertEqual(res2["valor"], "teste1")

    def test_connection_context_manager_rollback_em_excecao(self):
        with self.db.connection() as conn:
            conn.execute("CREATE TABLE teste_rb (id INTEGER PRIMARY KEY, valor TEXT)")

        with self.assertRaises(RuntimeError):
            with self.db.connection() as conn:
                conn.execute("INSERT INTO teste_rb (valor) VALUES ('nao_deve_persistir')")
                raise RuntimeError("Erro forçado para teste de rollback")

        with self.db.connection() as conn:
            res = conn.execute("SELECT COUNT(*) FROM teste_rb").fetchone()[0]
            self.assertEqual(res, 0)

    def test_inicializacao_cria_diretorio_se_necessario(self):
        subpasta = os.path.join(self.temp_dir.name, "subdir", "aninhado")
        caminho_aninhado = os.path.join(subpasta, "aninhado.db")
        db_aninhado = Database(caminho_aninhado)

        self.assertFalse(os.path.exists(subpasta))
        db_aninhado.inicializar(carregar_demo=False)
        self.assertTrue(os.path.exists(subpasta))
        self.assertTrue(os.path.exists(caminho_aninhado))

    def test_inicializacao_sem_demo(self):
        self.db.inicializar(carregar_demo=False)
        with self.db.connection() as conn:
            # Domínios devem existir
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM papel").fetchone()[0], 6)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM tipo_compromisso").fetchone()[0], 5)
            # Tabelas de dados devem estar zeradas
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM avaliacao").fetchone()[0], 0)

    def test_inicializacao_com_demo_nao_duplica_quando_ja_populado(self):
        self.db.inicializar(carregar_demo=True)
        with self.db.connection() as conn:
            total_compromissos = conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0]
            total_avaliacoes = conn.execute("SELECT COUNT(*) FROM avaliacao").fetchone()[0]
            self.assertEqual(total_compromissos, 5)
            self.assertEqual(total_avaliacoes, 3)

        # Rodar novamente não deve duplicar registros demo
        self.db.inicializar(carregar_demo=True)
        with self.db.connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0], total_compromissos)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM avaliacao").fetchone()[0], total_avaliacoes)


if __name__ == "__main__":
    unittest.main()
