"""Testes de integração Controller + Model + View via Router (sem rede)."""

from backend.router import Router
from tests.helpers import PAYLOAD_AVALIACAO, PAYLOAD_COMPROMISSO, BancoTemporarioTestCase


class RouterTest(BancoTemporarioTestCase):
    def setUp(self):
        super().setUp()
        self.router = Router(self.db)

    def test_saude(self):
        self.assertEqual(self.router.despachar("GET", "/api/saude"), (200, {"status": "ok"}))

    def test_listar_compromissos_contrato_json(self):
        status, lista = self.router.despachar("GET", "/api/compromissos")
        self.assertEqual(status, 200)
        self.assertEqual(
            set(lista[0]),
            {"id", "nome", "papel", "tipo", "tipo_label", "mensagem", "apoios", "data", "criado_em"},
        )
        self.assertRegex(lista[0]["data"], r"^\d{2}/\d{2}/\d{4}$")

    def test_criar_e_apoiar_compromisso(self):
        status, novo = self.router.despachar("POST", "/api/compromissos", PAYLOAD_COMPROMISSO)
        self.assertEqual(status, 201)
        status, apoiado = self.router.despachar("POST", f"/api/compromissos/{novo['id']}/apoios")
        self.assertEqual(status, 200)
        self.assertEqual(apoiado["apoios"], 2)

    def test_criar_compromisso_invalido_retorna_400_com_campos(self):
        status, payload = self.router.despachar("POST", "/api/compromissos", {"nome": ""})
        self.assertEqual(status, 400)
        self.assertIn("nome", payload["campos"])

    def test_apoiar_inexistente_retorna_404(self):
        status, payload = self.router.despachar("POST", "/api/compromissos/12345/apoios")
        self.assertEqual(status, 404)
        self.assertIn("erro", payload)

    def test_endpoint_inexistente_e_metodo_incorreto(self):
        self.assertEqual(self.router.despachar("GET", "/api/nada")[0], 404)
        self.assertEqual(self.router.despachar("DELETE", "/api/compromissos")[0], 405)
        self.assertEqual(self.router.despachar("GET", "/api/compromissos/1/apoios")[0], 405)

    def test_barra_final_e_tolerada(self):
        self.assertEqual(self.router.despachar("GET", "/api/compromissos/")[0], 200)

    def test_avaliacoes_e_metricas(self):
        status, _ = self.router.despachar("POST", "/api/avaliacoes", PAYLOAD_AVALIACAO)
        self.assertEqual(status, 201)
        status, metricas = self.router.despachar("GET", "/api/metricas")
        self.assertEqual(status, 200)
        self.assertEqual(metricas["total_avaliacoes"], 4)
        self.assertEqual(metricas["total_compromissos"], 5)
        self.assertEqual(metricas["total_apoios"], 196)
        self.assertIn("Docente Universitário(a)", metricas["distribuicao_papeis"])
