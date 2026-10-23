#!/usr/bin/env bash
# ==============================================================================
# MenHelpHer / EquiTech ODS 5 - Script Dinâmico de Inicialização e Testes (Docker)
# Projeto Integrado Transdisciplinar (PIT I e PIT II) - Engenharia de Software
# Instituição: Universidade Cruzeiro do Sul
# Autor: Julio Costa
# ==============================================================================

set -e

COR_AZUL="\033[1;34m"
COR_VERDE="\033[1;32m"
COR_AMARELO="\033[1;33m"
COR_VERMELHO="\033[1;31m"
COR_CIANO="\033[1;36m"
SEM_COR="\033[0m"

imprimir_banner() {
    clear 2>/dev/null || true
    echo -e "${COR_AZUL}==================================================================${SEM_COR}"
    echo -e "${COR_VERDE}  🚀 MenHelpHer / EquiTech ODS 5 - Ambiente Conteinerizado Docker${SEM_COR}"
    echo -e "${COR_CIANO}  Instituição:${SEM_COR} Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)"
    echo -e "${COR_CIANO}  Autor / Aluno:${SEM_COR} Julio Costa"
    echo -e "${COR_CIANO}  Disciplinas:${SEM_COR} PIT I e PIT II - Engenharia de Software"
    echo -e "${COR_AZUL}==================================================================${SEM_COR}"
}

imprimir_banner

# -----------------------------------------------------------------------------
# 1. Verificação / Instalação do Docker e Docker Compose
# -----------------------------------------------------------------------------
if ! command -v docker &> /dev/null; then
    echo -e "${COR_AMARELO}⚠️ Docker não foi detectado no sistema.${SEM_COR}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "Deseja que o script tente instalar o Docker automaticamente via repositório oficial? (s/N)"
        read -r resposta
        if [[ "$resposta" =~ ^[sS]$ ]]; then
            echo -e "${COR_CIANO}>> Instalando Docker via script oficial (pode solicitar senha sudo)...${SEM_COR}"
            curl -fsSL https://get.docker.com | sh
            sudo usermod -aG docker "$USER" || true
            echo -e "${COR_VERDE}✅ Docker instalado com sucesso!${SEM_COR}"
        else
            echo -e "${COR_VERMELHO}Instalação abortada. Instale o Docker Desktop ou pacote 'docker.io' manualmente.${SEM_COR}"
            exit 1
        fi
    else
        echo -e "${COR_VERMELHO}Por favor, instale o Docker Desktop para seu sistema operacional (https://www.docker.com/products/docker-desktop) e tente novamente.${SEM_COR}"
        exit 1
    fi
fi

# -----------------------------------------------------------------------------
# 2. Verificação do Serviço Docker (Daemon)
# -----------------------------------------------------------------------------
if ! docker info &> /dev/null; then
    echo -e "${COR_AMARELO}⚠️ O daemon do Docker não parece estar ativo. Tentando iniciar o serviço...${SEM_COR}"
    if command -v systemctl &> /dev/null; then
        sudo systemctl start docker || true
    elif command -v service &> /dev/null; then
        sudo service docker start || true
    fi
    sleep 2
    if ! docker info &> /dev/null; then
        echo -e "${COR_VERMELHO}❌ Não foi possível comunicar com o Docker. Inicie o Docker Desktop ou o serviço manualmente: 'sudo systemctl start docker'.${SEM_COR}"
        exit 1
    fi
fi

# -----------------------------------------------------------------------------
# 3. Liberação de Conflito de Porta (se porta 8000 estiver presa)
# -----------------------------------------------------------------------------
if lsof -i :8000 &> /dev/null; then
    echo -e "${COR_AMARELO}ℹ️ A porta 8000 está em uso. Verificando processo...${SEM_COR}"
    # Se for o próprio container, seguimos normalmente
    if ! docker ps | grep -q "menhelpher-app"; then
        echo -e "${COR_AMARELO}Liberando porta 8000 ocupada por processo local...${SEM_COR}"
        fuser -k 8000/tcp 2>/dev/null || true
        sleep 1
    fi
fi

# -----------------------------------------------------------------------------
# 4. Construção e Inicialização do Contêiner
# -----------------------------------------------------------------------------
echo -e "\n${COR_CIANO}>> Construindo e iniciando o contêiner MenHelpHer...${SEM_COR}"
docker compose up -d --build

echo -e "\n${COR_AMARELO}>> Aguardando verificação de saúde da aplicação (/api/saude)...${SEM_COR}"
tentativas=0
max_tentativas=15
saude_ok=false

while [ $tentativas -lt $max_tentativas ]; do
    if curl -s -f http://localhost:8000/api/saude &> /dev/null; then
        saude_ok=true
        break
    fi
    sleep 1
    tentativas=$((tentativas + 1))
    echo -n "."
done

echo ""
if [ "$saude_ok" = true ]; then
    echo -e "${COR_VERDE}✅ Contêiner ativo e saudável na porta 8000!${SEM_COR}"
else
    echo -e "${COR_VERMELHO}❌ O contêiner subiu, mas a verificação de saúde demorou a responder. Verificando logs:${SEM_COR}"
    docker compose logs --tail=20
    exit 1
fi

# -----------------------------------------------------------------------------
# 5. Abertura do Navegador
# -----------------------------------------------------------------------------
URL="http://localhost:8000"
echo -e "\n${COR_VERDE}👉 Aplicação pronta para testes em: ${COR_CIANO}${URL}${SEM_COR}"

if command -v xdg-open &> /dev/null; then
    xdg-open "$URL" &> /dev/null &
elif command -v open &> /dev/null; then
    open "$URL" &> /dev/null &
elif command -v powershell.exe &> /dev/null; then
    powershell.exe -c "Start-Process '$URL'" &> /dev/null &
fi

# -----------------------------------------------------------------------------
# 6. Menu Interativo para o Testador
# -----------------------------------------------------------------------------
while true; do
    echo -e "\n${COR_AZUL}------------------------------------------------------------------${SEM_COR}"
    echo -e "${COR_VERDE}📋 MENU DINÂMICO DO TESTADOR${SEM_COR}"
    echo -e "  [1] 🌐 Reabrir a aplicação no navegador (${URL})"
    echo -e "  [2] 🧪 Executar suíte de testes unitários (106 testes) DENTRO do contêiner"
    echo -e "  [3] 📜 Ver logs do servidor em tempo real (Ctrl+C para voltar ao menu)"
    echo -e "  [4] 🔄 Reinicializar banco de dados do contêiner (Limpar e repovoar demo)"
    echo -e "  [5] 🛑 Parar contêiner e sair"
    echo -e "${COR_AZUL}------------------------------------------------------------------${SEM_COR}"
    read -p "Escolha uma opção [1-5]: " opcao

    case "$opcao" in
        1)
            echo -e "${COR_CIANO}Abrindo ${URL}...${SEM_COR}"
            if command -v xdg-open &> /dev/null; then
                xdg-open "$URL" &> /dev/null &
            elif command -v open &> /dev/null; then
                open "$URL" &> /dev/null &
            fi
            ;;
        2)
            echo -e "\n${COR_CIANO}>> Executando suíte com 106 testes e cobertura de código no contêiner:${SEM_COR}"
            docker compose exec menhelpher pytest --cov=backend --cov-report=term-missing
            ;;
        3)
            echo -e "\n${COR_CIANO}>> Exibindo logs (Pressione Ctrl+C para retornar ao menu):${SEM_COR}\n"
            docker compose logs -f menhelpher || true
            ;;
        4)
            echo -e "\n${COR_AMARELO}>> Resetando banco de dados para os valores padrão de seed...${SEM_COR}"
            docker compose exec menhelpher rm -f /app/database/menhelpher.db
            docker compose restart menhelpher
            sleep 2
            echo -e "${COR_VERDE}✅ Banco de dados SQLite reinicializado com sucesso!${SEM_COR}"
            ;;
        5)
            echo -e "\n${COR_AMARELO}>> Parando contêiner...${SEM_COR}"
            docker compose down
            echo -e "${COR_VERDE}✅ Contêiner finalizado com sucesso. Obrigado pelos testes!${SEM_COR}"
            exit 0
            ;;
        *)
            echo -e "${COR_VERMELHO}Opção inválida.${SEM_COR}"
            ;;
    esac
done
