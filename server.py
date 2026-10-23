#!/usr/bin/env python3
"""
MenHelpHer / EquiTech ODS 5 - Ponto de entrada da aplicação web
Projeto Integrado Transdisciplinar (PIT I e PIT II) - Engenharia de Software
Autor: Julio Costa

Uso:
    python3 server.py

Variáveis de ambiente opcionais:
    MENHELPHER_HOST (padrão 127.0.0.1)   MENHELPHER_PORT (padrão 8000)
    MENHELPHER_DB   (caminho do arquivo SQLite)
"""

from backend import config
from backend.http_server import criar_servidor


def main():
    servidor = criar_servidor()
    host, porta = servidor.server_address[:2]
    print("=" * 64)
    print(" EquiTech ODS 5 - Portal MenHelpHer em execução!")
    print(" Projeto Integrado Transdisciplinar - Engenharia de Software")
    print(" Aluno: Julio Costa")
    print(f" Banco de dados: {config.DATABASE_PATH}")
    print(f" Acesse no navegador: http://localhost:{porta}")
    print("=" * 64)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado com sucesso.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
