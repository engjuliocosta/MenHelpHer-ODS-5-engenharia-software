# MenHelpHer — EquiTech ODS 5

Plataforma web interativa e campanha de sensibilização sobre Igualdade de Gênero em TI (ODS 5 da ONU).

## Visão geral
Este repositório contém a estrutura inicial de um projeto web em Python/Django para a campanha "EquiTech ODS 5".

## Estrutura inicial
- docs/
- src/
- tests/
- requirements.txt

## Execução local
```bash
git clone https://github.com/engjuliocosta/MenHelpHer-ODS-5-engenharia-software.git
cd MenHelpHer-ODS-5-engenharia-software
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```
