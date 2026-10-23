#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
MenHelpHer / EquiTech ODS 5 - Inicializador Universal Multiplataforma
Projeto Integrado Transdisciplinar (PIT I e PIT II) - Engenharia de Software
Instituição: Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)
Discente / Autor: Julio Costa

FINALIDADE DESTE SCRIPT:
Este arquivo independente (.py) pode ser enviado por e-mail, Google Drive,
WhatsApp ou baixado avulso por avaliadores e testadores.

Ao ser executado em QUALQUER sistema (Windows, Linux ou macOS), ele:
1. Detecta automaticamente o Sistema Operacional e arquitetura.
2. Verifica se o repositório do projeto já existe na pasta atual; caso não
   exista, faz o download automático do repositório no GitHub.
3. Verifica se o Docker / Docker Compose está disponível:
   - Se SIM: Constrói e inicializa o contêiner isolado da aplicação.
   - Se NÃO: Aciona o modo nativo Python como fallback automático, garantindo
     que NENHUM avaliador fique travado sem conseguir testar.
4. Aguarda a verificação de saúde da API (healthcheck em /api/saude).
5. Abre automaticamente o navegador padrão na URL da aplicação.
6. Oferece um menu interativo completo no terminal (execução de 106 testes,
   logs, reset de banco de dados e encerramento).
==============================================================================
"""

import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
import zipfile

# Metadados e URLs do Projeto
REPO_GIT_URL = "https://github.com/engjuliocosta/MenHelpHer-ODS-5-engenharia-software.git"
REPO_ZIP_URL = "https://github.com/engjuliocosta/MenHelpHer-ODS-5-engenharia-software/archive/refs/heads/main.zip"
PORTA_PADRAO = 8000
URL_APP = f"http://localhost:{PORTA_PADRAO}"
URL_SAUDE = f"{URL_APP}/api/saude"


def limpar_tela():
    """Limpa a tela do terminal de acordo com o sistema operacional."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def imprimir_banner():
    """Exibe o cabeçalho acadêmico e de identificação do projeto."""
    limpar_tela()
    print("=" * 70)
    print(" 🚀 MenHelpHer / EquiTech ODS 5 - Inicializador Universal de Testes")
    print(" Instituição: Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)")
    print(" Autor / Discente: Julio Costa")
    print(" Disciplinas: PIT I e PIT II - Engenharia de Software")
    print(f" Sistema Operacional Detectado: {platform.system()} ({platform.release()})")
    print(f" Versão do Python: {platform.python_version()}")
    print("=" * 70)
    print()


def comando_existe(comando):
    """Verifica se um executável existe no PATH do sistema."""
    return shutil.which(comando) is not None


def verificar_ou_baixar_repositorio():
    """Garante que os arquivos do projeto estejam disponíveis no diretório atual."""
    # Se já estiver dentro da pasta do projeto
    if os.path.exists("server.py") and os.path.isdir("backend"):
        print("✅ Arquivos do projeto identificados no diretório atual.")
        return os.getcwd()

    pasta_alvo = "MenHelpHer-ODS-5-engenharia-software"
    if os.path.exists(pasta_alvo) and os.path.exists(os.path.join(pasta_alvo, "server.py")):
        print(f"✅ Repositório já encontrado em ./{pasta_alvo}.")
        os.chdir(pasta_alvo)
        return os.getcwd()

    print("📥 Repositório não encontrado localmente.")
    print(">> Baixando arquivos do projeto automaticamente...")

    # Tentativa 1: Via Git Clone
    if comando_existe("git"):
        print(f">> Executando git clone de {REPO_GIT_URL}...")
        try:
            subprocess.run(["git", "clone", REPO_GIT_URL, pasta_alvo], check=True)
            os.chdir(pasta_alvo)
            print("✅ Clonagem concluída com sucesso!")
            return os.getcwd()
        except subprocess.CalledProcessError:
            print("⚠️ Falha no git clone. Tentando download direto do ZIP...")

    # Tentativa 2: Download direto do arquivo ZIP (caso não tenha Git)
    zip_dest = "repo_menhelpher.zip"
    print(f">> Baixando pacote ZIP oficial do GitHub ({REPO_ZIP_URL})...")
    try:
        urllib.request.urlretrieve(REPO_ZIP_URL, zip_dest)
        print(">> Extraindo arquivos...")
        with zipfile.ZipFile(zip_dest, "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove(zip_dest)

        pasta_extraida = "MenHelpHer-ODS-5-engenharia-software-main"
        if os.path.exists(pasta_extraida):
            os.rename(pasta_extraida, pasta_alvo)
            os.chdir(pasta_alvo)
        elif os.path.exists(pasta_alvo):
            os.chdir(pasta_alvo)

        print("✅ Arquivos baixados e extraídos com sucesso!")
        return os.getcwd()
    except Exception as erro:
        print(f"❌ Erro crítico ao baixar repositório: {erro}")
        sys.exit(1)


def docker_esta_ativo():
    """Verifica se o Docker está instalado e com o daemon ativo."""
    if not comando_existe("docker"):
        return False
    try:
        resultado = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        return resultado.returncode == 0
    except Exception:
        return False


def testar_saude_api():
    """Realiza uma requisição HTTP para a rota /api/saude."""
    try:
        with urllib.request.urlopen(URL_SAUDE, timeout=2) as resposta:
            return resposta.status == 200
    except Exception:
        return False


def aguardar_servidor(max_segundos=20):
    """Aguarda o servidor responder OK na rota de healthcheck."""
    print(">> Aguardando verificação de saúde da aplicação (/api/saude)...", end="", flush=True)
    inicio = time.time()
    while time.time() - inicio < max_segundos:
        if testar_saude_api():
            print(" [OK]")
            return True
        print(".", end="", flush=True)
        time.sleep(1)
    print(" [Timeout]")
    return False


def abrir_navegador():
    """Abre o navegador padrão na URL da aplicação."""
    print(f"\n🌐 Abrindo aplicação no navegador: {URL_APP}")
    try:
        webbrowser.open(URL_APP)
    except Exception as erro:
        print(f"Acesse manualmente: {URL_APP} (Erro ao abrir automaticamente: {erro})")


def iniciar_com_docker():
    """Inicia a aplicação via Docker Compose."""
    print("\n🐳 Inicializando ambiente conteinerizado via Docker Compose...")
    comando = ["docker", "compose", "up", "-d", "--build"]
    subprocess.run(comando, check=True)
    return True


def parar_docker():
    """Encerra os contêineres Docker."""
    print("\n🛑 Encerrando contêineres Docker...")
    subprocess.run(["docker", "compose", "down"], check=False)


def iniciar_nativo():
    """Inicia o servidor diretamente em Python nativo (Modo Fallback ultrarrápido)."""
    print("\n🐍 Inicializando aplicação em Modo Nativo Python (Ponto de entrada: server.py)...")
    processo = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return processo


def executar_testes(modo_docker):
    """Executa a suíte completa de 106 testes automatizados com cobertura."""
    print("\n" + "=" * 70)
    print(" 🧪 EXECUTANDO SUÍTE COMPLETA DE 106 TESTES AUTOMATIZADOS")
    print("=" * 70)

    if modo_docker:
        print(">> Executando Pytest com cobertura DENTRO do contêiner Docker:")
        subprocess.run(
            ["docker", "compose", "exec", "menhelpher", "pytest", "--cov=backend", "--cov-report=term-missing"],
            check=False,
        )
    else:
        # Modo Nativo: testa se pytest está instalado, senão usa unittest padrão
        if comando_existe("pytest"):
            subprocess.run([sys.executable, "-m", "pytest", "-v", "--cov=backend", "--cov-report=term-missing"], check=False)
        else:
            print(">> Executando via módulo padrão unittest (100% nativo do Python):")
            subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], check=False)


def resetar_banco(modo_docker):
    """Apaga o banco atual para que o schema e seeds sejam recriados do zero."""
    print("\n🔄 Resetando banco de dados SQLite para os valores padrão de demonstração...")
    db_path = os.path.join("database", "menhelpher.db")
    if modo_docker:
        subprocess.run(["docker", "compose", "exec", "menhelpher", "rm", "-f", "/app/database/menhelpher.db"], check=False)
        subprocess.run(["docker", "compose", "restart", "menhelpher"], check=False)
    else:
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except Exception as e:
                print(f"Aviso ao remover banco: {e}")
    time.sleep(1)
    print("✅ Banco reinicializado com sucesso!")


def menu_interativo(modo_docker, processo_nativo=None):
    """Exibe o console interativo dinâmico para os testadores."""
    while True:
        print("\n" + "-" * 70)
        print(" 📋 MENU DINÂMICO DO AVALIADOR / TESTADOR")
        print(f" Modo em Execução: {'🐳 Contêiner Docker' if modo_docker else '🐍 Python Nativo'}")
        print("  [1] 🌐 Reabrir a interface da aplicação no navegador")
        print("  [2] 🧪 Executar suíte de 106 testes unitários com relatório de cobertura")
        print("  [3] 📜 Ver logs do servidor em tempo real (Pressione Ctrl+C para voltar)")
        print("  [4] 🔄 Resetar banco de dados SQLite (Limpar e repovoar demo)")
        print("  [5] 🛑 Encerrar aplicação e sair")
        print("-" * 70)

        opcao = input("Escolha uma opção [1-5]: ").strip()

        if opcao == "1":
            abrir_navegador()
        elif opcao == "2":
            executar_testes(modo_docker)
        elif opcao == "3":
            if modo_docker:
                print("\n>> Exibindo logs do contêiner (Pressione Ctrl+C para retornar ao menu):")
                try:
                    subprocess.run(["docker", "compose", "logs", "-f", "menhelpher"])
                except KeyboardInterrupt:
                    pass
            else:
                print("\nℹ️ No modo nativo, a aplicação está rodando em segundo plano via PID:", processo_nativo.pid if processo_nativo else "N/A")
                print("Para ver requisições ativas, acesse os endpoints ou teste a API.")
        elif opcao == "4":
            resetar_banco(modo_docker)
        elif opcao == "5":
            print("\n🛑 Finalizando ambiente...")
            if modo_docker:
                parar_docker()
            elif processo_nativo:
                processo_nativo.terminate()
                processo_nativo.wait()
            print("✅ Aplicação finalizada. Obrigado por testar o projeto MenHelpHer!")
            break
        else:
            print("⚠️ Opção inválida. Digite um número de 1 a 5.")


def main():
    imprimir_banner()
    verificar_ou_baixar_repositorio()

    # Identificação do modo de execução ideal
    usar_docker = False
    processo_nativo = None

    if docker_esta_ativo():
        print("🐳 Docker e Docker Compose detectados e ativos!")
        try:
            iniciar_com_docker()
            usar_docker = True
        except Exception as erro:
            print(f"⚠️ Erro ao iniciar Docker ({erro}). Recorrendo ao Modo Nativo Python...")
            usar_docker = False

    if not usar_docker:
        print("🐍 Docker não disponível ou inativo. Executando em Modo Nativo Python...")
        processo_nativo = iniciar_nativo()

    # Verificação de saúde e abertura do navegador
    if aguardar_servidor():
        print(f"✅ Aplicação online e saudável na porta {PORTA_PADRAO}!")
        abrir_navegador()
    else:
        print(f"⚠️ Servidor iniciado, mas a rota {URL_SAUDE} não confirmou resposta a tempo.")
        print(f"Tente acessar manualmente no navegador: {URL_APP}")

    try:
        menu_interativo(modo_docker=usar_docker, processo_nativo=processo_nativo)
    except KeyboardInterrupt:
        print("\n\nSaindo...")
        if usar_docker:
            parar_docker()
        elif processo_nativo:
            processo_nativo.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()
