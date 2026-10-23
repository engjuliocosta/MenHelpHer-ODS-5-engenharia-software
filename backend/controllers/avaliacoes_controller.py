"""Controller: Avaliações de impacto."""

from ..views import serializar_avaliacao, serializar_lista


class AvaliacoesController:
    def __init__(self, model):
        self.model = model

    def listar(self, params=None, corpo=None):
        return 200, serializar_lista(self.model.listar(), serializar_avaliacao)

    def criar(self, params=None, corpo=None):
        return 201, serializar_avaliacao(self.model.criar(corpo))
