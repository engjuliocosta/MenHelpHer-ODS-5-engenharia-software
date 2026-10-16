#!/usr/bin/env python3
"""
MenHelpHer - Servidor de Aplicação Web
Projeto Integrado Transdisciplinar (PIT I)
Autor: Julio Costa
Curso: Engenharia de Software
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
COMPROMISSOS_FILE = os.path.join(DATA_DIR, 'compromissos.json')
AVALIACOES_FILE = os.path.join(DATA_DIR, 'avaliacoes.json')

os.makedirs(DATA_DIR, exist_ok=True)

def carregar_json(caminho, default_val):
    if not os.path.exists(caminho):
        return default_val
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_val

def salvar_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

class EquiTechHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/compromissos':
            compromissos = carregar_json(COMPROMISSOS_FILE, [])
            self.send_json_response(compromissos)
            return

        if path == '/api/avaliacoes':
            avaliacoes = carregar_json(AVALIACOES_FILE, [])
            self.send_json_response(avaliacoes)
            return

        if path == '/api/metricas':
            compromissos = carregar_json(COMPROMISSOS_FILE, [])
            avaliacoes = carregar_json(AVALIACOES_FILE, [])
            media_clareza = round(sum(a.get('clareza', 5) for a in avaliacoes) / max(len(avaliacoes), 1), 1)
            media_aprendizado = round(sum(a.get('aprendizado_vieses', 5) for a in avaliacoes) / max(len(avaliacoes), 1), 1)
            media_ods5 = round(sum(a.get('relevancia_ods5', 5) for a in avaliacoes) / max(len(avaliacoes), 1), 1)

            metricas = {
                "total_compromissos": len(compromissos),
                "total_apoios": sum(c.get('likes', 0) for c in compromissos),
                "total_avaliacoes": len(avaliacoes),
                "media_clareza": media_clareza,
                "media_aprendizado_vieses": media_aprendizado,
                "media_relevancia_ods5": media_ods5,
                "distribuicao_papeis": self.calcular_distribuicao_papeis(compromissos)
            }
            self.send_json_response(metricas)
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        try:
            dados = json.loads(body) if body else {}
        except Exception:
            self.send_error_response(400, "JSON inválido")
            return

        if path == '/api/compromissos':
            if not dados.get('nome') or not dados.get('mensagem'):
                self.send_error_response(400, "Nome e mensagem são obrigatórios")
                return

            compromissos = carregar_json(COMPROMISSOS_FILE, [])
            novo = {
                "id": f"comp-{int(datetime.now().timestamp() * 1000)}",
                "nome": dados.get('nome', '').strip(),
                "papel": dados.get('papel', 'Estudante'),
                "tipo": dados.get('tipo', 'Geral'),
                "tipo_label": dados.get('tipo_label', 'Apoio à Equidade'),
                "mensagem": dados.get('mensagem', '').strip(),
                "data": datetime.now().strftime("%d/%m/%Y"),
                "likes": 1
            }
            compromissos.insert(0, novo)
            salvar_json(COMPROMISSOS_FILE, compromissos)
            self.send_json_response(novo, status=201)
            return

        if path == '/api/compromissos/like':
            cid = dados.get('id')
            compromissos = carregar_json(COMPROMISSOS_FILE, [])
            atualizado = False
            for comp in compromissos:
                if comp.get('id') == cid:
                    comp['likes'] = comp.get('likes', 0) + 1
                    atualizado = True
                    break
            if atualizado:
                salvar_json(COMPROMISSOS_FILE, compromissos)
                self.send_json_response({"sucesso": True})
            else:
                self.send_error_response(404, "Compromisso não encontrado")
            return

        if path == '/api/avaliacoes':
            avaliacoes = carregar_json(AVALIACOES_FILE, [])
            nova_av = {
                "id": f"av-{int(datetime.now().timestamp() * 1000)}",
                "perfil": dados.get('perfil', 'Estudante'),
                "clareza": int(dados.get('clareza', 5)),
                "aprendizado_vieses": int(dados.get('aprendizado_vieses', 5)),
                "relevancia_ods5": int(dados.get('relevancia_ods5', 5)),
                "comentario": dados.get('comentario', '').strip(),
                "data": datetime.now().strftime("%d/%m/%Y")
            }
            avaliacoes.insert(0, nova_av)
            salvar_json(AVALIACOES_FILE, avaliacoes)
            self.send_json_response(nova_av, status=201)
            return

        self.send_error_response(404, "Endpoint não encontrado")

    def send_json_response(self, data, status=200):
        content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_error_response(self, status, mensagem):
        self.send_json_response({"erro": mensagem}, status=status)

    def calcular_distribuicao_papeis(self, compromissos):
        contagem = {}
        for c in compromissos:
            p = c.get('papel', 'Outro')
            contagem[p] = contagem.get(p, 0) + 1
        return contagem

def main():
    os.chdir(BASE_DIR)
    with socketserver.TCPServer(("", PORT), EquiTechHandler) as httpd:
        print(f"================================================================")
        print(f" EquiTech ODS 5 - Portal MenHelpHer em execução!")
        print(f" Projeto Integrado Transdisciplinar - Engenharia de Software")
        print(f" Aluno: Julio Cezar Costa Alves (RGM: 39909549)")
        print(f" Acesse no navegador: http://localhost:{PORT}")
        print(f"================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado com sucesso.")

if __name__ == '__main__':
    main()
