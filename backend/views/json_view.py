"""View: transforma registros do banco em representações JSON para a API.

Mantém o contrato público da API independente do esquema físico do banco.
"""

from datetime import datetime


def _data_br(criado_em):
    try:
        return datetime.strptime(criado_em, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return ""


def serializar_compromisso(registro):
    return {
        "id": registro["id"],
        "nome": registro["nome"],
        "papel": registro["papel"],
        "tipo": registro["tipo"],
        "tipo_label": registro["tipo_label"],
        "mensagem": registro["mensagem"],
        "apoios": registro["apoios"],
        "data": _data_br(registro["criado_em"]),
        "criado_em": registro["criado_em"],
    }


def serializar_avaliacao(registro):
    return {
        "id": registro["id"],
        "perfil": registro["perfil"],
        "clareza": registro["clareza"],
        "aprendizado_vieses": registro["aprendizado_vieses"],
        "relevancia_ods5": registro["relevancia_ods5"],
        "comentario": registro["comentario"],
        "data": _data_br(registro["criado_em"]),
        "criado_em": registro["criado_em"],
    }


def serializar_lista(registros, serializador):
    return [serializador(registro) for registro in registros]


def serializar_metricas(compromissos, avaliacoes):
    return {
        "total_compromissos": compromissos["total"],
        "total_apoios": compromissos["apoios"],
        "distribuicao_papeis": compromissos["distribuicao_papeis"],
        "total_avaliacoes": avaliacoes["total"],
        "media_clareza": avaliacoes["media_clareza"],
        "media_aprendizado_vieses": avaliacoes["media_aprendizado_vieses"],
        "media_relevancia_ods5": avaliacoes["media_relevancia_ods5"],
    }
