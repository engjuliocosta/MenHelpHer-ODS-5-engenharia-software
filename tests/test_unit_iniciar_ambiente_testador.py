"""Testes unitários para o script universal iniciar_ambiente_testador.py."""

import unittest
from unittest.mock import MagicMock, patch

import iniciar_ambiente_testador as init_script


class IniciarAmbienteTestadorUnitTest(unittest.TestCase):
    """Testa métodos auxiliares de detecção e inicialização do script universal."""

    def test_comando_existe_identifica_binarios(self):
        self.assertTrue(init_script.comando_existe("python3") or init_script.comando_existe("python"))
        self.assertFalse(init_script.comando_existe("comando_inexistente_123456"))

    @patch("shutil.which")
    def test_docker_esta_ativo_retorna_falso_se_docker_nao_instalado(self, mock_which):
        mock_which.return_value = None
        self.assertFalse(init_script.docker_esta_ativo())

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_docker_esta_ativo_retorna_true_quando_daemon_responde(self, mock_run, mock_which):
        mock_which.return_value = "/usr/bin/docker"
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(init_script.docker_esta_ativo())

    @patch("urllib.request.urlopen")
    def test_testar_saude_api_sucesso(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        self.assertTrue(init_script.testar_saude_api())

    @patch("urllib.request.urlopen")
    def test_testar_saude_api_falha(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Conexão recusada")
        self.assertFalse(init_script.testar_saude_api())

    @patch("webbrowser.open")
    def test_abrir_navegador(self, mock_browser):
        init_script.abrir_navegador()
        mock_browser.assert_called_once_with(init_script.URL_APP)


if __name__ == "__main__":
    unittest.main()
