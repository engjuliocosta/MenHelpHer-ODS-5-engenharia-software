"""Servidor HTTP: serve o front-end estático e encaminha /api/* ao Router."""

import functools
import json
import logging
import socketserver
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from . import config
from .database import Database
from .errors import PayloadTooLargeError, ValidationError
from .router import Router

logger = logging.getLogger(__name__)


class EquiTechHandler(SimpleHTTPRequestHandler):
    router = None  # definido em criar_servidor()

    # ----------------------------------------------------------- cabeçalhos --
    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        if self.path.startswith("/api/"):
            # CORS liberado apenas para a API (permite abrir o index.html via file://).
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Cache-Control", "no-store")
        else:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    # --------------------------------------------------------------- verbos --
    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self._eh_api():
            self._responder_api("GET")
        else:
            super().do_GET()

    def do_HEAD(self):
        if self._eh_api():
            self.send_error(405)
        else:
            super().do_HEAD()

    def do_POST(self):
        if self._eh_api():
            self._responder_api("POST")
        else:
            self.send_error(405)

    # ------------------------------------------------------------- internos --
    def _eh_api(self):
        return urlparse(self.path).path.startswith("/api/")

    def _ler_corpo_json(self):
        try:
            tamanho = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise ValidationError("Cabeçalho Content-Length inválido.")
        if tamanho > config.MAX_BODY_BYTES:
            raise PayloadTooLargeError("Corpo da requisição excede o limite permitido.")
        if tamanho == 0:
            return {}
        try:
            return json.loads(self.rfile.read(tamanho).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValidationError("JSON inválido.")

    def _responder_api(self, metodo):
        caminho = urlparse(self.path).path
        try:
            corpo = self._ler_corpo_json() if metodo == "POST" else None
            status, payload = self.router.despachar(metodo, caminho, corpo)
        except (ValidationError, PayloadTooLargeError) as erro:
            status, payload = erro.status, {"erro": erro.mensagem}
        except Exception:  # falha inesperada: não vaza detalhes ao cliente
            logger.exception("Erro interno ao processar %s %s", metodo, caminho)
            status, payload = 500, {"erro": "Erro interno do servidor."}
        self._enviar_json(status, payload)

    def _enviar_json(self, status, payload):
        conteudo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)


def criar_servidor(host=None, porta=None, db=None):
    """Monta o servidor HTTP multithread. ``porta=0`` escolhe uma porta livre (testes)."""
    db = db or Database()
    db.inicializar()
    handler = type("Handler", (EquiTechHandler,), {"router": Router(db)})
    handler = functools.partial(handler, directory=config.FRONTEND_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    servidor = ThreadingHTTPServer(
        (host if host is not None else config.HOST, config.PORT if porta is None else porta),
        handler,
    )
    servidor.daemon_threads = True
    return servidor
