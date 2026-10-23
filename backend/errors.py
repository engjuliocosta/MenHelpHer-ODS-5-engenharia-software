"""Exceções de domínio traduzidas em respostas HTTP pelo roteador."""


class AppError(Exception):
    status = 500

    def __init__(self, mensagem, campos=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campos = campos or {}


class ValidationError(AppError):
    status = 400


class NotFoundError(AppError):
    status = 404


class PayloadTooLargeError(AppError):
    status = 413


class MethodNotAllowedError(AppError):
    status = 405
