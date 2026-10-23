"""Controller: Mural de Compromissos. Devolve tuplas (status HTTP, payload)."""

from ..views import serializar_compromisso, serializar_lista


class CompromissosController:
    def __init__(self, model):
        self.model = model

    def listar(self, params=None, corpo=None):
        return 200, serializar_lista(self.model.listar(), serializar_compromisso)

    def criar(self, params=None, corpo=None):
        return 201, serializar_compromisso(self.model.criar(corpo))

    def apoiar(self, params, corpo=None):
        return 200, serializar_compromisso(self.model.apoiar(int(params["id"])))
