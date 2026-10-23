"""Testes unitários isolados para backend/http_server.py (EquiTechHandler e criar_servidor)."""

import io
import json
import unittest
from unittest.mock import MagicMock, patch

from backend import config
from backend.errors import PayloadTooLargeError, ValidationError
from backend.http_server import EquiTechHandler, criar_servidor


class EquiTechHandlerUnitTest(unittest.TestCase):
    """Testa métodos internos do EquiTechHandler usando mocks de socket/request."""

    def _criar_handler(self, path="/api/saude", headers=None, rfile_bytes=b""):
        """Monta uma instância leve de EquiTechHandler sem abrir portas de rede."""
        handler = EquiTechHandler.__new__(EquiTechHandler)
        handler.path = path
        handler.headers = headers or {}
        handler.rfile = io.BytesIO(rfile_bytes)
        handler.wfile = io.BytesIO()
        handler.router = MagicMock()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        return handler

    def test_eh_api_identifica_rotas_corretamente(self):
        handler_api = self._criar_handler(path="/api/compromissos?filtro=1")
        self.assertTrue(handler_api._eh_api())

        handler_estatico = self._criar_handler(path="/index.html")
        self.assertFalse(handler_estatico._eh_api())

    def test_ler_corpo_json_valido(self):
        dados = {"nome": "Ada Lovelace"}
        corpo_bytes = json.dumps(dados).encode("utf-8")
        handler = self._criar_handler(
            path="/api/compromissos",
            headers={"Content-Length": str(len(corpo_bytes))},
            rfile_bytes=corpo_bytes,
        )
        resultado = handler._ler_corpo_json()
        self.assertEqual(resultado, dados)

    def test_ler_corpo_json_vazio_quando_content_length_zero(self):
        handler = self._criar_handler(
            path="/api/compromissos",
            headers={"Content-Length": "0"},
            rfile_bytes=b"",
        )
        self.assertEqual(handler._ler_corpo_json(), {})

    def test_ler_corpo_json_content_length_invalido(self):
        handler = self._criar_handler(
            path="/api/compromissos",
            headers={"Content-Length": "invalido"},
        )
        with self.assertRaises(ValidationError) as ctx:
            handler._ler_corpo_json()
        self.assertIn("Content-Length inválido", str(ctx.exception))

    def test_ler_corpo_json_payload_maior_que_limite(self):
        tamanho_excessivo = config.MAX_BODY_BYTES + 1
        handler = self._criar_handler(
            path="/api/compromissos",
            headers={"Content-Length": str(tamanho_excessivo)},
        )
        with self.assertRaises(PayloadTooLargeError) as ctx:
            handler._ler_corpo_json()
        self.assertIn("excede o limite", str(ctx.exception))

    def test_ler_corpo_json_corpo_com_sintaxe_invalida(self):
        corpo_malformado = b"[{nome: quebrado"
        handler = self._criar_handler(
            path="/api/compromissos",
            headers={"Content-Length": str(len(corpo_malformado))},
            rfile_bytes=corpo_malformado,
        )
        with self.assertRaises(ValidationError) as ctx:
            handler._ler_corpo_json()
        self.assertIn("JSON inválido", str(ctx.exception))

    def test_do_options_retorna_204(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler.do_OPTIONS()
        handler.send_response.assert_called_once_with(204)
        handler.end_headers.assert_called_once()

    def test_responder_api_captura_validation_error(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler._ler_corpo_json = MagicMock(side_effect=ValidationError("Campo ausente"))
        handler._enviar_json = MagicMock()

        handler._responder_api("POST")
        handler._enviar_json.assert_called_once_with(400, {"erro": "Campo ausente"})

    def test_responder_api_captura_payload_too_large(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler._ler_corpo_json = MagicMock(side_effect=PayloadTooLargeError("Payload gigante"))
        handler._enviar_json = MagicMock()

        handler._responder_api("POST")
        handler._enviar_json.assert_called_once_with(413, {"erro": "Payload gigante"})

    def test_responder_api_trata_excecao_inesperada_com_500(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler.router.despachar.side_effect = RuntimeError("Falha não tratada")
        handler._enviar_json = MagicMock()

        handler._responder_api("GET")
        handler._enviar_json.assert_called_once_with(500, {"erro": "Erro interno do servidor."})

    def test_enviar_json_escreve_resposta_no_wfile(self):
        handler = self._criar_handler(path="/api/saude")
        handler._enviar_json(200, {"status": "ok"})

        handler.send_response.assert_called_once_with(200)
        self.assertTrue(handler.send_header.called)
        handler.end_headers.assert_called_once()
        conteudo_gravado = handler.wfile.getvalue().decode("utf-8")
        self.assertEqual(json.loads(conteudo_gravado), {"status": "ok"})

    def test_do_head_em_rota_de_api_retorna_405(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler.send_error = MagicMock()
        handler.do_HEAD()
        handler.send_error.assert_called_once_with(405)

    def test_do_head_em_rota_estatica_chama_super_do_head(self):
        handler = self._criar_handler(path="/index.html")
        with patch.object(EquiTechHandler.__bases__[0], "do_HEAD") as mock_super_head:
            handler.do_HEAD()
            mock_super_head.assert_called_once()

    def test_do_post_em_rota_estatica_retorna_405(self):
        handler = self._criar_handler(path="/index.html")
        handler.send_error = MagicMock()
        handler.do_POST()
        handler.send_error.assert_called_once_with(405)

    def test_do_get_em_rota_de_api_invoca_responder_api(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler._responder_api = MagicMock()
        handler.do_GET()
        handler._responder_api.assert_called_once_with("GET")

    def test_do_post_em_rota_de_api_invoca_responder_api(self):
        handler = self._criar_handler(path="/api/compromissos")
        handler._responder_api = MagicMock()
        handler.do_POST()
        handler._responder_api.assert_called_once_with("POST")

    def test_end_headers_aplica_cabecalhos_especificos_para_api_e_estatico(self):
        # Validação para rota de API
        handler_api = self._criar_handler(path="/api/metricas")
        cabecalhos_api = {}
        handler_api.send_header = lambda k, v: cabecalhos_api.setdefault(k, v)
        with patch.object(EquiTechHandler.__bases__[0], "end_headers"):
            EquiTechHandler.end_headers(handler_api)

        self.assertEqual(cabecalhos_api.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(cabecalhos_api.get("X-Frame-Options"), "DENY")
        self.assertEqual(cabecalhos_api.get("Referrer-Policy"), "no-referrer")
        self.assertEqual(cabecalhos_api.get("Access-Control-Allow-Origin"), "*")
        self.assertEqual(cabecalhos_api.get("Cache-Control"), "no-store")

        # Validação para rota estática
        handler_estatico = self._criar_handler(path="/style.css")
        cabecalhos_estatico = {}
        handler_estatico.send_header = lambda k, v: cabecalhos_estatico.setdefault(k, v)
        with patch.object(EquiTechHandler.__bases__[0], "end_headers"):
            EquiTechHandler.end_headers(handler_estatico)

        self.assertEqual(cabecalhos_estatico.get("Cache-Control"), "no-cache")
        self.assertNotIn("Access-Control-Allow-Origin", cabecalhos_estatico)


class CriarServidorUnitTest(unittest.TestCase):
    """Testa a função de fábrica do servidor HTTP."""

    @patch("backend.http_server.Database")
    @patch("backend.http_server.ThreadingHTTPServer")
    def test_criar_servidor_monta_servidor_com_defaults(self, mock_server, mock_db_class):
        mock_db_instance = MagicMock()
        mock_db_class.return_value = mock_db_instance

        servidor = criar_servidor(host="127.0.0.1", porta=0, db=mock_db_instance)

        mock_db_instance.inicializar.assert_called_once()
        mock_server.assert_called_once()
        self.assertIsNotNone(servidor)


if __name__ == "__main__":
    unittest.main()
