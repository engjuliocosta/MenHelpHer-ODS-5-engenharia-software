"""Testes de integração ponta a ponta: servidor HTTP real em porta efêmera."""

import http.client
import json
import threading

from backend import config
from backend.http_server import EquiTechHandler, criar_servidor
from tests.helpers import PAYLOAD_AVALIACAO, PAYLOAD_COMPROMISSO, BancoTemporarioTestCase


class ServidorHttpTest(BancoTemporarioTestCase):
    def setUp(self):
        super().setUp()
        # Silencia o log de acesso para manter a saída dos testes limpa.
        antigo = EquiTechHandler.log_message
        EquiTechHandler.log_message = lambda *args, **kwargs: None
        self.addCleanup(setattr, EquiTechHandler, "log_message", antigo)
        self.servidor = criar_servidor(host="127.0.0.1", porta=0, db=self.db)
        self.porta = self.servidor.server_address[1]
        thread = threading.Thread(target=self.servidor.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        thread.start()
        self.addCleanup(self._encerrar)

    def _encerrar(self):
        self.servidor.shutdown()
        self.servidor.server_close()

    def requisitar(self, metodo, caminho, corpo=None, cabecalhos=None, bruto=None):
        conexao = http.client.HTTPConnection("127.0.0.1", self.porta, timeout=5)
        dados = bruto if bruto is not None else (json.dumps(corpo) if corpo is not None else None)
        cab = {"Content-Type": "application/json"} if dados is not None else {}
        cab.update(cabecalhos or {})
        conexao.request(metodo, caminho, body=dados, headers=cab)
        resposta = conexao.getresponse()
        texto = resposta.read().decode("utf-8")
        conexao.close()
        return resposta, texto

    # ---------------------------------------------------------- estáticos --
    def test_serve_pagina_inicial(self):
        resposta, texto = self.requisitar("GET", "/")
        self.assertEqual(resposta.status, 200)
        self.assertIn("MenHelpHer", texto)

    def test_serve_css_e_js(self):
        self.assertEqual(self.requisitar("GET", "/css/main.css")[0].status, 200)
        self.assertEqual(self.requisitar("GET", "/js/app.js")[0].status, 200)

    def test_nao_expoe_codigo_do_servidor_banco_nem_git(self):
        for caminho in (
            "/server.py",
            "/backend/config.py",
            "/database/schema.sql",
            "/database/menhelpher.db",
            "/.git/config",
            "/../server.py",
            "/%2e%2e/server.py",
        ):
            resposta, _ = self.requisitar("GET", caminho)
            self.assertEqual(resposta.status, 404, caminho)

    def test_cabecalhos_de_seguranca(self):
        resposta, _ = self.requisitar("GET", "/")
        self.assertEqual(resposta.getheader("X-Content-Type-Options"), "nosniff")
        self.assertEqual(resposta.getheader("X-Frame-Options"), "DENY")

    # ---------------------------------------------------------------- API --
    def test_api_lista_compromissos(self):
        resposta, texto = self.requisitar("GET", "/api/compromissos")
        self.assertEqual(resposta.status, 200)
        self.assertIn("application/json", resposta.getheader("Content-Type"))
        self.assertEqual(resposta.getheader("Access-Control-Allow-Origin"), "*")
        self.assertEqual(len(json.loads(texto)), 5)

    def test_api_fluxo_criar_apoiar_e_persistir(self):
        resposta, texto = self.requisitar("POST", "/api/compromissos", PAYLOAD_COMPROMISSO)
        self.assertEqual(resposta.status, 201)
        novo = json.loads(texto)
        resposta, texto = self.requisitar("POST", f"/api/compromissos/{novo['id']}/apoios")
        self.assertEqual(json.loads(texto)["apoios"], 2)
        lista = json.loads(self.requisitar("GET", "/api/compromissos")[1])
        self.assertEqual(lista[0]["id"], novo["id"])

    def test_api_armazena_xss_como_texto_sem_executar(self):
        payload = {**PAYLOAD_COMPROMISSO, "nome": "<script>alert(1)</script>"}
        resposta, texto = self.requisitar("POST", "/api/compromissos", payload)
        self.assertEqual(resposta.status, 201)
        self.assertEqual(json.loads(texto)["nome"], "<script>alert(1)</script>")
        self.assertIn("application/json", resposta.getheader("Content-Type"))

    def test_api_avaliacao_e_metricas(self):
        resposta, _ = self.requisitar("POST", "/api/avaliacoes", PAYLOAD_AVALIACAO)
        self.assertEqual(resposta.status, 201)
        metricas = json.loads(self.requisitar("GET", "/api/metricas")[1])
        self.assertEqual(metricas["total_avaliacoes"], 4)

    def test_api_json_invalido_retorna_400(self):
        resposta, texto = self.requisitar("POST", "/api/compromissos", bruto="{nao-e-json")
        self.assertEqual(resposta.status, 400)
        self.assertIn("erro", json.loads(texto))

    def test_api_validacao_retorna_400_com_campos(self):
        resposta, texto = self.requisitar("POST", "/api/avaliacoes", {"perfil": "x"})
        self.assertEqual(resposta.status, 400)
        self.assertIn("clareza", json.loads(texto)["campos"])

    def test_api_corpo_muito_grande_retorna_413(self):
        grande = json.dumps({"nome": "x" * (config.MAX_BODY_BYTES + 10)})
        resposta, _ = self.requisitar("POST", "/api/compromissos", bruto=grande)
        self.assertEqual(resposta.status, 413)

    def test_api_404_e_405(self):
        self.assertEqual(self.requisitar("GET", "/api/inexistente")[0].status, 404)
        self.assertEqual(self.requisitar("POST", "/api/metricas", {})[0].status, 405)

    def test_api_options_cors_preflight(self):
        resposta, _ = self.requisitar("OPTIONS", "/api/compromissos")
        self.assertEqual(resposta.status, 204)
        self.assertIn("POST", resposta.getheader("Access-Control-Allow-Methods"))
