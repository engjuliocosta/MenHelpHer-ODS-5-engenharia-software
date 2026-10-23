"""Testes unitários da camada Model (regras de negócio e integridade do banco)."""

import sqlite3

from backend.errors import NotFoundError, ValidationError
from backend.models import AvaliacaoModel, CompromissoModel
from tests.helpers import PAYLOAD_AVALIACAO, PAYLOAD_COMPROMISSO, BancoTemporarioTestCase


class BancoDeDadosTest(BancoTemporarioTestCase):
    def test_banco_novo_carrega_catalogos_e_demo(self):
        with self.db.connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM papel").fetchone()[0], 6)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM tipo_compromisso").fetchone()[0], 5)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0], 5)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM avaliacao").fetchone()[0], 3)

    def test_inicializacao_e_idempotente(self):
        self.db.inicializar()
        self.db.inicializar()
        with self.db.connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM papel").fetchone()[0], 6)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM compromisso").fetchone()[0], 5)

    def test_chave_estrangeira_e_imposta(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db.connection() as conn:
                conn.execute(
                    "INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem) "
                    "VALUES ('Fulana', 999, 1, 'mensagem valida aqui')"
                )

    def test_check_de_nota_e_imposto(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db.connection() as conn:
                conn.execute(
                    "INSERT INTO avaliacao (perfil_id, clareza, aprendizado_vieses, relevancia_ods5) "
                    "VALUES (1, 9, 1, 1)"
                )

    def test_rollback_em_caso_de_erro(self):
        try:
            with self.db.connection() as conn:
                conn.execute("INSERT INTO papel (nome) VALUES ('Temporario')")
                raise RuntimeError("falha simulada")
        except RuntimeError:
            pass
        with self.db.connection() as conn:
            self.assertIsNone(conn.execute("SELECT 1 FROM papel WHERE nome='Temporario'").fetchone())


class CompromissoModelTest(BancoTemporarioTestCase):
    def setUp(self):
        super().setUp()
        self.model = CompromissoModel(self.db)

    def test_listar_retorna_mais_recentes_primeiro(self):
        lista = self.model.listar()
        self.assertEqual(len(lista), 5)
        datas = [c["criado_em"] for c in lista]
        self.assertEqual(datas, sorted(datas, reverse=True))

    def test_criar_compromisso_valido(self):
        novo = self.model.criar(PAYLOAD_COMPROMISSO)
        self.assertEqual(novo["nome"], "Ada Teste")
        self.assertEqual(novo["apoios"], 1)
        self.assertEqual(novo["tipo_label"], "Mentoria & Apoio")
        self.assertEqual(len(self.model.listar()), 6)

    def test_criar_remove_espacos_das_bordas(self):
        novo = self.model.criar({**PAYLOAD_COMPROMISSO, "nome": "  Ada Teste  "})
        self.assertEqual(novo["nome"], "Ada Teste")

    def test_validacao_campos_obrigatorios(self):
        with self.assertRaises(ValidationError) as ctx:
            self.model.criar({})
        self.assertEqual(set(ctx.exception.campos), {"nome", "mensagem", "papel", "tipo"})

    def test_validacao_mensagem_curta_e_longa(self):
        for mensagem in ("curta", "x" * 501):
            with self.assertRaises(ValidationError) as ctx:
                self.model.criar({**PAYLOAD_COMPROMISSO, "mensagem": mensagem})
            self.assertIn("mensagem", ctx.exception.campos)

    def test_validacao_papel_e_tipo_desconhecidos(self):
        with self.assertRaises(ValidationError) as ctx:
            self.model.criar({**PAYLOAD_COMPROMISSO, "papel": "Hacker", "tipo": "Outro"})
        self.assertEqual(set(ctx.exception.campos), {"papel", "tipo"})

    def test_payload_que_nao_e_objeto(self):
        with self.assertRaises(ValidationError):
            self.model.criar(["lista"])

    def test_apoiar_incrementa_contador(self):
        antes = self.model.listar()[0]
        depois = self.model.apoiar(antes["id"])
        self.assertEqual(depois["apoios"], antes["apoios"] + 1)

    def test_apoiar_inexistente(self):
        with self.assertRaises(NotFoundError):
            self.model.apoiar(99999)

    def test_sql_injection_e_tratado_como_texto(self):
        nome = "Robert'); DROP TABLE compromisso;--"
        novo = self.model.criar({**PAYLOAD_COMPROMISSO, "nome": nome})
        self.assertEqual(novo["nome"], nome)
        self.assertEqual(len(self.model.listar()), 6)

    def test_estatisticas(self):
        est = self.model.estatisticas()
        self.assertEqual(est["total"], 5)
        self.assertEqual(est["apoios"], 29 + 42 + 35 + 51 + 39)
        self.assertEqual(sum(est["distribuicao_papeis"].values()), 5)


class AvaliacaoModelTest(BancoTemporarioTestCase):
    def setUp(self):
        super().setUp()
        self.model = AvaliacaoModel(self.db)

    def test_criar_avaliacao_valida(self):
        nova = self.model.criar(PAYLOAD_AVALIACAO)
        self.assertEqual(nova["perfil"], "Estudante")
        self.assertEqual(nova["clareza"], 5)
        self.assertEqual(len(self.model.listar()), 4)

    def test_notas_como_texto_numerico_sao_aceitas(self):
        nova = self.model.criar({**PAYLOAD_AVALIACAO, "clareza": "3"})
        self.assertEqual(nova["clareza"], 3)

    def test_notas_invalidas(self):
        for valor in (0, 6, -1, "abc", None, True, 2.5 * 4):
            with self.assertRaises(ValidationError, msg=repr(valor)) as ctx:
                self.model.criar({**PAYLOAD_AVALIACAO, "clareza": valor})
            self.assertIn("clareza", ctx.exception.campos)

    def test_perfil_invalido(self):
        with self.assertRaises(ValidationError) as ctx:
            self.model.criar({**PAYLOAD_AVALIACAO, "perfil": "Alienígena"})
        self.assertIn("perfil", ctx.exception.campos)

    def test_comentario_opcional_mas_limitado(self):
        self.assertEqual(self.model.criar({**PAYLOAD_AVALIACAO, "comentario": ""})["comentario"], "")
        with self.assertRaises(ValidationError):
            self.model.criar({**PAYLOAD_AVALIACAO, "comentario": "x" * 501})

    def test_estatisticas_medias(self):
        est = self.model.estatisticas()
        self.assertEqual(est["total"], 3)
        self.assertEqual(est["media_clareza"], 5.0)
        self.assertEqual(est["media_aprendizado_vieses"], 4.7)


class AvaliacaoSemDadosTest(BancoTemporarioTestCase):
    carregar_demo = False

    def test_medias_nulas_quando_nao_ha_avaliacoes(self):
        est = AvaliacaoModel(self.db).estatisticas()
        self.assertEqual(est["total"], 0)
        self.assertIsNone(est["media_clareza"])
