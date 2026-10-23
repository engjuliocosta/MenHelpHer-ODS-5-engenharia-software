#!/usr/bin/env bash
# ==============================================================================
# MenHelpHer / EquiTech ODS 5 - Script de Execução da Suíte de Testes
# Instituição: Universidade Cruzeiro do Sul
# Discente: Julio Costa
# ==============================================================================

set -e

echo "=================================================================="
echo " 🧪 MenHelpHer / EquiTech ODS 5 - Executando Suíte de Testes"
echo " Instituição: Universidade Cruzeiro do Sul"
echo " Discente: Julio Costa"
echo "=================================================================="

if command -v pytest &> /dev/null; then
    echo ">> Executando suíte com Pytest e Cobertura de Código:"
    pytest --cov=backend --cov-report=term-missing
else
    echo ">> Pytest não detectado. Executando via módulo nativo unittest (Python 3):"
    python3 -m unittest discover -s tests -t . -v
fi

echo "=================================================================="
echo " ✅ Todos os testes executados com sucesso!"
echo "=================================================================="
