"""Model: Avaliações de impacto da campanha (Etapa 5 do PIT)."""

from ..errors import ValidationError

COMENTARIO_MAX = 500
CAMPOS_NOTA = ("clareza", "aprendizado_vieses", "relevancia_ods5")

_SELECT = """
    SELECT a.id, pa.nome AS perfil, a.clareza, a.aprendizado_vieses,
           a.relevancia_ods5, a.comentario, a.criado_em
      FROM avaliacao a
      JOIN perfil_avaliador pa ON pa.id = a.perfil_id
"""


def _nota(valor):
    """Converte para inteiro de 1 a 5; devolve None se inválido."""
    if isinstance(valor, bool):
        return None
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if 1 <= numero <= 5 else None


class AvaliacaoModel:
    def __init__(self, db):
        self.db = db

    def validar(self, dados):
        if not isinstance(dados, dict):
            raise ValidationError("Corpo da requisição inválido.")

        erros = {}
        perfil = str(dados.get("perfil") or "").strip()
        comentario = str(dados.get("comentario") or "").strip()

        with self.db.connection() as conn:
            perfil_row = conn.execute(
                "SELECT id FROM perfil_avaliador WHERE nome = ?", (perfil,)
            ).fetchone()
        if perfil_row is None:
            erros["perfil"] = "Perfil inválido."

        notas = {}
        for campo in CAMPOS_NOTA:
            notas[campo] = _nota(dados.get(campo))
            if notas[campo] is None:
                erros[campo] = "A nota deve ser um número inteiro de 1 a 5."

        if len(comentario) > COMENTARIO_MAX:
            erros["comentario"] = f"O comentário deve ter no máximo {COMENTARIO_MAX} caracteres."

        if erros:
            raise ValidationError("Dados inválidos.", erros)
        return {"perfil_id": perfil_row["id"], "comentario": comentario, **notas}

    def listar(self):
        with self.db.connection() as conn:
            return [
                dict(linha)
                for linha in conn.execute(_SELECT + " ORDER BY a.criado_em DESC, a.id DESC")
            ]

    def buscar(self, avaliacao_id):
        with self.db.connection() as conn:
            return dict(conn.execute(_SELECT + " WHERE a.id = ?", (avaliacao_id,)).fetchone())

    def criar(self, dados):
        limpo = self.validar(dados)
        with self.db.connection() as conn:
            cursor = conn.execute(
                """INSERT INTO avaliacao
                       (perfil_id, clareza, aprendizado_vieses, relevancia_ods5, comentario)
                   VALUES (:perfil_id, :clareza, :aprendizado_vieses, :relevancia_ods5, :comentario)""",
                limpo,
            )
            novo_id = cursor.lastrowid
        return self.buscar(novo_id)

    def estatisticas(self):
        with self.db.connection() as conn:
            linha = conn.execute(
                """SELECT COUNT(*) AS total,
                          ROUND(AVG(clareza), 1) AS clareza,
                          ROUND(AVG(aprendizado_vieses), 1) AS vieses,
                          ROUND(AVG(relevancia_ods5), 1) AS ods5
                     FROM avaliacao"""
            ).fetchone()
        return {
            "total": linha["total"],
            "media_clareza": linha["clareza"],
            "media_aprendizado_vieses": linha["vieses"],
            "media_relevancia_ods5": linha["ods5"],
        }
