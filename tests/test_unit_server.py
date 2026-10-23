"""Testes unitários para o script de inicialização server.py."""

import io
import unittest
from unittest.mock import MagicMock, patch

import server


class ServerUnitTest(unittest.TestCase):
    """Testa o ponto de entrada principal server.py."""

    @patch("server.criar_servidor")
    def test_main_executa_e_encerra_ao_receber_keyboard_interrupt(self, mock_criar_servidor):
        mock_servidor = MagicMock()
        mock_servidor.server_address = ("127.0.0.1", 8000)
        mock_servidor.serve_forever.side_effect = KeyboardInterrupt
        mock_criar_servidor.return_value = mock_servidor

        saida_capturada = io.StringIO()
        with patch("sys.stdout", saida_capturada):
            server.main()

        texto_saida = saida_capturada.getvalue()
        self.assertIn("Universidade Cruzeiro do Sul", texto_saida)
        self.assertIn("Julio Costa", texto_saida)
        self.assertIn("http://localhost:8000", texto_saida)
        self.assertIn("Servidor encerrado com sucesso", texto_saida)

        mock_criar_servidor.assert_called_once()
        mock_servidor.serve_forever.assert_called_once()
        mock_servidor.server_close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
