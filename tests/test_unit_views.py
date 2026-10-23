"""Testes estritamente unitários da camada View (backend/views/json_view.py).

Verifica a serialização e a formatação defensiva de dados para JSON sem tocar no banco.
"""

import unittest

from backend.views.json_view import (
    _data_br,
    serializar_avaliacao,
    serializar_compromisso,
    serializar_lista,
    serializar_metricas,
)


class JsonViewUnitTest(unittest.TestCase):
    def test_data_br_formato_padrao(self):
        self.assertEqual(_data_br("2026-10-16 14:30:00"), "16/10/2026")
        self.assertEqual(_data_br("2026-01-01 00:00:00"), "01/01/2026")

    def test_data_br_entradas_invalidas_retornam_string_vazia(self):
        self.assertEqual(_data_br("data-invalida"), "")
        self.assertEqual(_data_br(""), "")
        self.assertEqual(_data_br(None), "")
        self.assertEqual(_data_br(12345), "")

    def test_serializar_compromisso_estrutura_completa(self):
        registro = {
            "id": 42,
            "nome": "Julio Costa",
            "papel": "Estudante de Engenharia de Software",
            "tipo": "Code Review Inclusivo",
            "tipo_label": "Revisão Respeitosa",
            "mensagem": "Comprometo-me a revisar PRs com empatia e respeito.",
            "apoios": 15,
            "criado_em": "2026-10-20 10:00:00",
        }
        saida = serializar_compromisso(registro)
        self.assertEqual(
            saida,
            {
                "id": 42,
                "nome": "Julio Costa",
                "papel": "Estudante de Engenharia de Software",
                "tipo": "Code Review Inclusivo",
                "tipo_label": "Revisão Respeitosa",
                "mensagem": "Comprometo-me a revisar PRs com empatia e respeito.",
                "apoios": 15,
                "data": "20/10/2026",
                "criado_em": "2026-10-20 10:00:00",
            },
        )

    def test_serializar_avaliacao_estrutura_completa(self):
        registro = {
            "id": 7,
            "perfil": "Docente Universitário(a)",
            "clareza": 5,
            "aprendizado_vieses": 4,
            "relevancia_ods5": 5,
            "comentario": "Excelente trabalho acadêmico.",
            "criado_em": "2026-10-21 15:30:00",
        }
        saida = serializar_avaliacao(registro)
        self.assertEqual(
            saida,
            {
                "id": 7,
                "perfil": "Docente Universitário(a)",
                "clareza": 5,
                "aprendizado_vieses": 4,
                "relevancia_ods5": 5,
                "comentario": "Excelente trabalho acadêmico.",
                "data": "21/10/2026",
                "criado_em": "2026-10-21 15:30:00",
            },
        )

    def test_serializar_lista(self):
        itens = [{"nome": "A"}, {"nome": "B"}]
        resultado = serializar_lista(itens, lambda x: x["nome"].lower())
        self.assertEqual(resultado, ["a", "b"])
        self.assertEqual(serializar_lista([], lambda x: x), [])

    def test_serializar_metricas(self):
        comp_stats = {
            "total": 10,
            "apoios": 120,
            "distribuicao_papeis": {"Estudante": 6, "Docente": 4},
        }
        aval_stats = {
            "total": 5,
            "media_clareza": 4.8,
            "media_aprendizado_vieses": 4.6,
            "media_relevancia_ods5": 5.0,
        }
        resultado = serializar_metricas(comp_stats, aval_stats)
        self.assertEqual(resultado["total_compromissos"], 10)
        self.assertEqual(resultado["total_apoios"], 120)
        self.assertEqual(resultado["distribuicao_papeis"], {"Estudante": 6, "Docente": 4})
        self.assertEqual(resultado["total_avaliacoes"], 5)
        self.assertEqual(resultado["media_clareza"], 4.8)
        self.assertEqual(resultado["media_aprendizado_vieses"], 4.6)
        self.assertEqual(resultado["media_relevancia_ods5"], 5.0)


if __name__ == "__main__":
    unittest.main()
