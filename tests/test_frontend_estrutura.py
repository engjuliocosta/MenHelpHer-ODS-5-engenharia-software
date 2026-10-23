"""Testes estáticos do front-end: integridade do HTML, referências e consistência com o banco."""

import os
import re
import unittest
from html.parser import HTMLParser

from backend import config
from backend.database import Database
from tests.helpers import BancoTemporarioTestCase

INDEX = os.path.join(config.FRONTEND_DIR, "index.html")


class _Coletor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.scripts = []
        self.styles = []
        self.opcoes = {}  # id do select -> [valores]
        self.h1 = 0
        self.imagens_sem_alt = 0
        self._select = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "script" and "src" in a:
            self.scripts.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.imagens_sem_alt += 1
        if tag == "select":
            self._select = a.get("id")
            self.opcoes[self._select] = []
        if tag == "option" and self._select:
            self.opcoes[self._select].append(a.get("value"))

    def handle_endtag(self, tag):
        if tag == "select":
            self._select = None


def _ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


class IndexHtmlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = _ler(INDEX)
        cls.coletor = _Coletor()
        cls.coletor.feed(cls.html)

    def test_ids_sao_unicos(self):
        repetidos = {i for i in self.coletor.ids if self.coletor.ids.count(i) > 1}
        self.assertEqual(repetidos, set())

    def test_possui_um_unico_h1_e_idioma(self):
        self.assertEqual(self.coletor.h1, 1)
        self.assertIn('lang="pt-BR"', self.html)

    def test_arquivos_referenciados_existem(self):
        for caminho in self.coletor.scripts + self.coletor.styles:
            self.assertTrue(
                os.path.isfile(os.path.join(config.FRONTEND_DIR, caminho)), caminho
            )

    def test_ordem_dos_scripts_respeita_dependencias(self):
        nomes = [os.path.basename(s) for s in self.coletor.scripts]
        for antes, depois in [("utils.js", "mural.js"), ("api.js", "mural.js"), ("data.js", "app.js"), ("mural.js", "app.js")]:
            self.assertLess(nomes.index(antes), nomes.index(depois), f"{antes} deve vir antes de {depois}")

    def test_ids_usados_pelo_javascript_existem_no_html(self):
        usados = set()
        for arquivo in ("app.js", "mural.js", "dashboard.js"):
            usados |= set(re.findall(r"getElementById\('([^']+)'\)", _ler(os.path.join(config.FRONTEND_DIR, "js", arquivo))))
        ausentes = {i for i in usados if i not in self.coletor.ids}
        # elementos criados dinamicamente pelo simulador/mural não fazem parte do HTML estático
        ausentes -= {"feedbackBox", "feedbackTitle", "feedbackText"}
        self.assertEqual(ausentes, set())

    def test_campos_de_formulario_tem_rotulo(self):
        for campo in ("committerName", "committerRole", "commitmentType", "commitmentMsg",
                      "evalPerfil", "evalClareza", "evalVieses", "evalOds", "evalComentario"):
            self.assertRegex(self.html, rf'<label for="{campo}"', campo)

    def test_possui_link_de_salto_para_conteudo(self):
        self.assertIn('class="skip-link"', self.html)
        self.assertIn('id="mainContentArea"', self.html)

    def test_mural_nao_usa_handlers_inline(self):
        # O mural usa delegação de eventos: nenhum onclick com dados vindos do usuário.
        self.assertNotIn("MuralModule.", self.html)
        self.assertNotIn("onclick=", _ler(os.path.join(config.FRONTEND_DIR, "js", "mural.js")))


class ConsistenciaHtmlBancoTest(BancoTemporarioTestCase):
    """Os valores das <option> precisam existir nos catálogos do banco (senão a API rejeita)."""

    @classmethod
    def setUpClass(cls):
        cls.coletor = _Coletor()
        cls.coletor.feed(_ler(INDEX))

    def _catalogo(self, sql):
        with self.db.connection() as conn:
            return {linha[0] for linha in conn.execute(sql)}

    def test_papeis_do_formulario_existem_no_banco(self):
        self.assertEqual(set(self.coletor.opcoes["committerRole"]), self._catalogo("SELECT nome FROM papel"))

    def test_tipos_do_formulario_existem_no_banco(self):
        self.assertEqual(set(self.coletor.opcoes["commitmentType"]), self._catalogo("SELECT codigo FROM tipo_compromisso"))

    def test_perfis_da_avaliacao_existem_no_banco(self):
        self.assertEqual(set(self.coletor.opcoes["evalPerfil"]), self._catalogo("SELECT nome FROM perfil_avaliador"))

    def test_rotulos_data_label_coincidem_com_o_banco(self):
        html = _ler(INDEX)
        pares = re.findall(r'<option value="([^"]+)" data-label="([^"]+)"', html)
        self.assertEqual(len(pares), 5)
        with self.db.connection() as conn:
            for codigo, rotulo in pares:
                esperado = conn.execute("SELECT rotulo FROM tipo_compromisso WHERE codigo=?", (codigo,)).fetchone()[0]
                self.assertEqual(rotulo.replace("&amp;", "&"), esperado)
