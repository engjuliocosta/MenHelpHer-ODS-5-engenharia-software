"""Roteador da API REST: associa método + caminho a ações dos controllers."""

import re

from .controllers import AvaliacoesController, CompromissosController, MetricasController
from .database import Database
from .errors import AppError, MethodNotAllowedError, NotFoundError
from .models import AvaliacaoModel, CompromissoModel


class Router:
    def __init__(self, db=None):
        self.db = db or Database()
        compromissos = CompromissoModel(self.db)
        avaliacoes = AvaliacaoModel(self.db)
        c = CompromissosController(compromissos)
        a = AvaliacoesController(avaliacoes)
        m = MetricasController(compromissos, avaliacoes)

        self.rotas = [
            ("GET", r"/api/saude", m.saude),
            ("GET", r"/api/metricas", m.metricas),
            ("GET", r"/api/compromissos", c.listar),
            ("POST", r"/api/compromissos", c.criar),
            ("POST", r"/api/compromissos/(?P<id>\d+)/apoios", c.apoiar),
            ("GET", r"/api/avaliacoes", a.listar),
            ("POST", r"/api/avaliacoes", a.criar),
        ]

    def despachar(self, metodo, caminho, corpo=None):
        """Retorna (status, payload). Erros de domínio viram respostas JSON."""
        caminho = caminho.rstrip("/") or "/"
        try:
            caminho_existe = False
            for metodo_rota, padrao, acao in self.rotas:
                encontrou = re.fullmatch(padrao, caminho)
                if not encontrou:
                    continue
                caminho_existe = True
                if metodo_rota == metodo:
                    return acao(encontrou.groupdict(), corpo)
            if caminho_existe:
                raise MethodNotAllowedError("Método não permitido para este endpoint.")
            raise NotFoundError("Endpoint não encontrado.")
        except AppError as erro:
            payload = {"erro": erro.mensagem}
            if erro.campos:
                payload["campos"] = erro.campos
            return erro.status, payload
