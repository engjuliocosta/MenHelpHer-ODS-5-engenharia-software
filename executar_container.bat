@echo off
REM ==============================================================================
REM MenHelpHer / EquiTech ODS 5 - Script Dinamico de Inicializacao e Testes (Windows)
REM Projeto Integrado Transdisciplinar (PIT I e PIT II) - Engenharia de Software
REM Instituicao: Universidade Cruzeiro do Sul
REM Autor: Julio Costa
REM ==============================================================================

chcp 65001 >nul
cls
echo ==================================================================
echo   🚀 MenHelpHer / EquiTech ODS 5 - Ambiente Conteinerizado Docker
echo   Instituicao: Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)
echo   Autor / Aluno: Julio Costa
echo   Disciplinas: PIT I e PIT II - Engenharia de Software
echo ==================================================================
echo.

REM 1. Verifica se Docker esta instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Docker nao esta instalado ou nao esta no PATH do Windows.
    echo Baixe e instale o Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM 2. Verifica se Docker Daemon esta rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Docker Desktop nao esta em execucao.
    echo Por favor, abra o aplicativo Docker Desktop e aguarde inicializar.
    pause
    exit /b 1
)

echo [1/3] Construindo e iniciando conteiner via Docker Compose...
docker compose up -d --build
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao iniciar o conteiner Docker.
    pause
    exit /b 1
)

echo [2/3] Aguardando verificacao de saude da aplicacao...
timeout /t 4 /nobreak >nul

echo [3/3] Abrindo aplicacao no navegador padrao: http://localhost:8000
start http://localhost:8000

:MENU
echo.
echo ==================================================================
echo  📋 MENU DINAMICO DO TESTADOR (Windows)
echo ==================================================================
echo   [1] Reabrir no navegador (http://localhost:8000)
echo   [2] Executar suite de 106 testes unitarios DENTRO do conteiner
echo   [3] Ver logs do servidor em tempo real (Pressione Ctrl+C para voltar)
echo   [4] Reinicializar banco de dados SQLite (Limpar e repovoar demo)
echo   [5] Parar conteiner e sair
echo ==================================================================
set /p OPCAO="Escolha uma opcao [1-5]: "

if "%OPCAO%"=="1" (
    start http://localhost:8000
    goto MENU
)
if "%OPCAO%"=="2" (
    echo.
    echo Executando suite de 106 testes unitarios no conteiner...
    docker compose exec menhelpher pytest --cov=backend --cov-report=term-missing
    pause
    goto MENU
)
if "%OPCAO%"=="3" (
    echo.
    echo Exibindo logs (Pressione Ctrl+C para retornar):
    docker compose logs -f menhelpher
    goto MENU
)
if "%OPCAO%"=="4" (
    echo.
    echo Reiniciando banco de dados...
    docker compose exec menhelpher rm -f /app/database/menhelpher.db
    docker compose restart menhelpher
    echo Banco reinicializado com sucesso!
    goto MENU
)
if "%OPCAO%"=="5" (
    echo.
    echo Parando conteiner...
    docker compose down
    echo Conteiner finalizado. Obrigado pelos testes!
    exit /b 0
)

echo Opcao invalida.
goto MENU
