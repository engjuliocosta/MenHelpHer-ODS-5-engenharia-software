"""Testes estritamente unitários dos Controllers (backend/controllers/).

Usa objetos simulados (Mocks) para testar os controladores em isolamento
completo da camada de persistência e banco de dados.
"""

import unittest
from unittest.mock import MagicMock

from backend.controllers.avaliacoes_controller import AvaliacoesController
from backend.controllers.compromissos_controller import CompromissosController
from backend.controllers.metricas_controller import MetricasController


class CompromissosControllerUnitTest(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.controller = CompromissosController(self.mock_model)

    def test_listar_chama_model_e_retorna_200(self):
        self.mock_model.listar.return_value = [
            {
                "id": 1,
                "nome": "Julio Costa",
                "papel": "Estudante",
                "tipo": "Code Review",
                "tipo_label": "Revisão",
                "mensagem": "Texto do compromisso",
                "apoios": 5,
                "criado_em": "2026-10-16 12:00:00",
            }
        ]
        status, payload = self.controller.listar()
        self.assertEqual(status, 200)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["nome"], "Julio Costa")
        self.mock_model.listar.assert_called_once()

    def test_criar_chama_model_e_retorna_201(self):
        dados_entrada = {
            "nome": "Julio Costa",
            "papel": "Estudante",
            "tipo": "Mentoria Ativa",
            "mensagem": "Mensagem válida de compromisso",
        }
        self.mock_model.criar.return_value = {
            "id": 10,
            "nome": "Julio Costa",
            "papel": "Estudante",
            "tipo": "Mentoria Ativa",
            "tipo_label": "Mentoria & Apoio",
            "mensagem": "Mensagem válida de compromisso",
            "apoios": 1,
            "criado_em": "2026-10-23 10:00:00",
        }
        status, payload = self.controller.criar(corpo=dados_entrada)
        self.assertEqual(status, 201)
        self.assertEqual(payload["id"], 10)
        self.assertEqual(payload["data"], "23/10/2026")
        self.mock_model.criar.assert_called_once_with(dados_entrada)

    def test_apoiar_converte_id_e_retorna_200(self):
        self.mock_model.apoiar.return_value = {
            "id": 10,
            "nome": "Julio Costa",
            "papel": "Estudante",
            "tipo": "Mentoria Ativa",
            "tipo_label": "Mentoria & Apoio",
            "mensagem": "Mensagem",
            "apoios": 2,
            "criado_em": "2026-10-23 10:00:00",
        }
        status, payload = self.controller.apoiar(params={"id": "10"})
        self.assertEqual(status, 200)
        self.assertEqual(payload["apoios"], 2)
        self.mock_model.apoiar.assert_called_once_with(10)


class AvaliacoesControllerUnitTest(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.controller = AvaliacoesController(self.mock_model)

    def test_listar_chama_model_e_retorna_200(self):
        self.mock_model.listar.return_value = [
            {
                "id": 1,
                "perfil": "Docente",
                "clareza": 5,
                "aprendizado_vieses": 5,
                "relevancia_ods5": 5,
                "comentario": "Excelente",
                "criado_em": "2026-10-15 12:00:00",
            }
        ]
        status, payload = self.controller.listar()
        self.assertEqual(status, 200)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["perfil"], "Docente")
        self.mock_model.listar.assert_called_once()

    def test_criar_chama_model_e_retorna_201(self):
        dados = {
            "perfil": "Estudante",
            "clareza": 5,
            "aprendizado_vieses": 4,
            "relevancia_ods5": 5,
            "comentario": "Muito bom",
        }
        self.mock_model.criar.return_value = {
            "id": 2,
            "perfil": "Estudante",
            "clareza": 5,
            "aprendizado_vieses": 4,
            "relevancia_ods5": 5,
            "comentario": "Muito bom",
            "criado_em": "2026-10-23 10:00:00",
        }
        status, payload = self.controller.criar(corpo=dados)
        self.assertEqual(status, 201)
        self.assertEqual(payload["id"], 2)
        self.mock_model.criar.assert_called_once_with(dados)


class MetricasControllerUnitTest(unittest.TestCase):
    def setUp(self):
        self.mock_comp = MagicMock()
        self.mock_aval = MagicMock()
        self.controller = MetricasController(self.mock_comp, self.mock_aval)

    def test_metricas_combina_estatisticas_dos_models(self):
        self.mock_comp.estatisticas.return_value = {
            "total": 8,
            "apoios": 50,
            "distribuicao_papeis": {"Estudante": 8},
        }
        self.mock_aval.estatisticas.return_value = {
            "total": 4,
            "media_clareza": 5.0,
            "media_aprendizado_vieses": 4.5,
            "media_relevancia_ods5": 5.0,
        }
        status, payload = self.controller.metricas()
        self.assertEqual(status, 200)
        self.assertEqual(payload["total_compromissos"], 8)
        self.assertEqual(payload["total_avaliacoes"], 4)
        self.mock_comp.estatisticas.assert_called_once()
        self.mock_aval.estatisticas.assert_called_once()

    def test_saude_executa_consulta_e_retorna_ok(self):
        status, payload = self.controller.saude()
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"status": "ok"})
        self.mock_comp.estatisticas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
