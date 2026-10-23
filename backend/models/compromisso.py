"""Model: Compromissos do Mural HeForShe (regras de negócio + persistência)."""

from ..errors import NotFoundError, ValidationError

NOME_MIN, NOME_MAX = 2, 80
MENSAGEM_MIN, MENSAGEM_MAX = 10, 500

_SELECT = """
    SELECT c.id, c.nome, p.nome AS papel, t.codigo AS tipo, t.rotulo AS tipo_label,
           c.mensagem, c.apoios, c.criado_em
      FROM compromisso c
      JOIN papel p ON p.id = c.papel_id
      JOIN tipo_compromisso t ON t.id = c.tipo_id
"""


class CompromissoModel:
    def __init__(self, db):
        self.db = db

    # ------------------------------------------------------------- validação --
    def validar(self, dados):
        """Valida e normaliza o payload. Levanta ValidationError com os campos."""
        if not isinstance(dados, dict):
            raise ValidationError("Corpo da requisição inválido.")

        erros = {}
        nome = str(dados.get("nome") or "").strip()
        mensagem = str(dados.get("mensagem") or "").strip()
        papel = str(dados.get("papel") or "").strip()
        tipo = str(dados.get("tipo") or "").strip()

        if not NOME_MIN <= len(nome) <= NOME_MAX:
            erros["nome"] = f"Informe um nome com {NOME_MIN} a {NOME_MAX} caracteres."
        if not MENSAGEM_MIN <= len(mensagem) <= MENSAGEM_MAX:
            erros["mensagem"] = (
                f"A declaração deve ter entre {MENSAGEM_MIN} e {MENSAGEM_MAX} caracteres."
            )

        with self.db.connection() as conn:
            papel_row = conn.execute(
                "SELECT id FROM papel WHERE nome = ?", (papel,)
            ).fetchone()
            tipo_row = conn.execute(
                "SELECT id FROM tipo_compromisso WHERE codigo = ?", (tipo,)
            ).fetchone()
        if papel_row is None:
            erros["papel"] = "Papel inválido."
        if tipo_row is None:
            erros["tipo"] = "Tipo de compromisso inválido."

        if erros:
            raise ValidationError("Dados inválidos.", erros)
        return {
            "nome": nome,
            "mensagem": mensagem,
            "papel_id": papel_row["id"],
            "tipo_id": tipo_row["id"],
        }

    # ------------------------------------------------------------- consultas --
    def listar(self):
        with self.db.connection() as conn:
            linhas = conn.execute(_SELECT + " ORDER BY c.criado_em DESC, c.id DESC")
            return [dict(linha) for linha in linhas]

    def buscar(self, compromisso_id):
        with self.db.connection() as conn:
            linha = conn.execute(_SELECT + " WHERE c.id = ?", (compromisso_id,)).fetchone()
        if linha is None:
            raise NotFoundError("Compromisso não encontrado.")
        return dict(linha)

    def estatisticas(self):
        with self.db.connection() as conn:
            total, apoios = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(apoios), 0) FROM compromisso"
            ).fetchone()
            distribuicao = {
                linha["nome"]: linha["total"]
                for linha in conn.execute(
                    """SELECT p.nome, COUNT(*) AS total
                         FROM compromisso c JOIN papel p ON p.id = c.papel_id
                        GROUP BY p.nome ORDER BY total DESC, p.nome"""
                )
            }
        return {"total": total, "apoios": apoios, "distribuicao_papeis": distribuicao}

    # ---------------------------------------------------------------- escrita --
    def criar(self, dados):
        limpo = self.validar(dados)
        with self.db.connection() as conn:
            cursor = conn.execute(
                """INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios)
                   VALUES (:nome, :papel_id, :tipo_id, :mensagem, 1)""",
                limpo,
            )
            novo_id = cursor.lastrowid
        return self.buscar(novo_id)

    def apoiar(self, compromisso_id):
        with self.db.connection() as conn:
            cursor = conn.execute(
                "UPDATE compromisso SET apoios = apoios + 1 WHERE id = ?",
                (compromisso_id,),
            )
            if cursor.rowcount == 0:
                raise NotFoundError("Compromisso não encontrado.")
        return self.buscar(compromisso_id)
