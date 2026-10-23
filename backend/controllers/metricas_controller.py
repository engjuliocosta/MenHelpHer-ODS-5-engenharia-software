"""Controller: métricas consolidadas da campanha e verificação de saúde."""

from ..views import serializar_metricas


class MetricasController:
    def __init__(self, compromissos, avaliacoes):
        self.compromissos = compromissos
        self.avaliacoes = avaliacoes

    def metricas(self, params=None, corpo=None):
        return 200, serializar_metricas(
            self.compromissos.estatisticas(), self.avaliacoes.estatisticas()
        )

    def saude(self, params=None, corpo=None):
        self.compromissos.estatisticas()  # consulta simples: valida o acesso ao banco
        return 200, {"status": "ok"}
