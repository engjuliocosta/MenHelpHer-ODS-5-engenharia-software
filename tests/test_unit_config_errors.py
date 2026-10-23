"""Testes unitários para backend/config.py e backend/errors.py."""

import os
import unittest
from unittest.mock import patch

from backend import config
from backend.errors import (
    AppError,
    MethodNotAllowedError,
    NotFoundError,
    PayloadTooLargeError,
    ValidationError,
)


class ConfigUnitTest(unittest.TestCase):
    """Testa valores padrão e resoluções de caminho do backend/config.py."""

    def test_valores_padrao(self):
        self.assertIsInstance(config.BASE_DIR, str)
        self.assertTrue(os.path.isabs(config.BASE_DIR))
        self.assertEqual(config.MAX_BODY_BYTES, 16 * 1024)
        self.assertTrue(os.path.isdir(config.DATABASE_DIR))
        self.assertTrue(os.path.isdir(config.FRONTEND_DIR))
        self.assertTrue(os.path.isfile(config.SCHEMA_SQL))
        self.assertTrue(os.path.isfile(config.SEED_DOMINIOS_SQL))
        self.assertTrue(os.path.isfile(config.SEED_DEMO_SQL))

    def test_sobrescrita_por_variaveis_de_ambiente(self):
        with patch.dict(
            os.environ,
            {
                "MENHELPHER_HOST": "0.0.0.0",
                "MENHELPHER_PORT": "9090",
                "MENHELPHER_DB": "/tmp/custom_menhelpher.db",
            },
        ):
            # Recarrega módulo para validar leitura do ambiente
            import importlib
            import backend.config as cfg
            importlib.reload(cfg)

            self.assertEqual(cfg.HOST, "0.0.0.0")
            self.assertEqual(cfg.PORT, 9090)
            self.assertEqual(cfg.DATABASE_PATH, "/tmp/custom_menhelpher.db")

        # Restaura módulo com valores normais
        importlib.reload(config)


class ErrorsUnitTest(unittest.TestCase):
    """Testa hierarquia, mensagens e códigos HTTP da camada de exceções de domínio."""

    def test_app_error_base(self):
        err = AppError("Erro genérico", campos={"chave": "invalido"})
        self.assertIsInstance(err, Exception)
        self.assertEqual(err.status, 500)
        self.assertEqual(err.mensagem, "Erro genérico")
        self.assertEqual(err.campos, {"chave": "invalido"})
        self.assertEqual(str(err), "Erro genérico")

    def test_app_error_sem_campos_inicia_dicionario_vazio(self):
        err = AppError("Sem campos")
        self.assertEqual(err.campos, {})

    def test_validation_error(self):
        err = ValidationError("Dados inválidos", campos={"nome": "Obrigatório"})
        self.assertIsInstance(err, AppError)
        self.assertEqual(err.status, 400)
        self.assertEqual(err.mensagem, "Dados inválidos")
        self.assertEqual(err.campos, {"nome": "Obrigatório"})

    def test_not_found_error(self):
        err = NotFoundError("Registro não encontrado")
        self.assertIsInstance(err, AppError)
        self.assertEqual(err.status, 404)
        self.assertEqual(err.mensagem, "Registro não encontrado")

    def test_payload_too_large_error(self):
        err = PayloadTooLargeError("Excedeu limite de 16KB")
        self.assertIsInstance(err, AppError)
        self.assertEqual(err.status, 413)
        self.assertEqual(err.mensagem, "Excedeu limite de 16KB")

    def test_method_not_allowed_error(self):
        err = MethodNotAllowedError("Método não permitido")
        self.assertIsInstance(err, AppError)
        self.assertEqual(err.status, 405)
        self.assertEqual(err.mensagem, "Método não permitido")


if __name__ == "__main__":
    unittest.main()
