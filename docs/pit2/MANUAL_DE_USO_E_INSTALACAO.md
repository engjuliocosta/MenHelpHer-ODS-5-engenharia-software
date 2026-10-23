# Manual de Uso e Instalação da Aplicação
## MenHelpHer / EquiTech ODS 5 — Engenharia de Software

> **Projeto:** MenHelpHer — Plataforma de Equidade de Gênero na Engenharia de Software  
> **Componente Curricular:** PIT I e PIT II  
> **Autor:** Julio Cezar Costa Alves (Julio Costa) — RGM: 39909549  

---

## 1. Visão Geral do Sistema
O **MenHelpHer / EquiTech ODS 5** é um sistema web responsivo e acessível concebido sob a arquitetura **Model-View-Controller (MVC)**. Ele fornece ferramentas interativas para combater vieses inconscientes e promover a paridade de gênero no setor de tecnologia, integrando:
- Painel de Indicadores e Visualização de Dados Oficiais (SBC, IPEA, Inep e ONU Mulheres).
- Simulador Gamificado de Dilemas Éticos e Vieses Inconscientes.
- Mural Digital de Compromissos (Movimento HeForShe) com persistência em SGBD relacional.
- Galeria de Pioneiras da Computação e Checklist de Boas Práticas para Squads.
- Módulo de Avaliação de Impacto da Campanha e Métricas Consolidadas.

---

## 2. Pré-requisitos de Instalação e Execução
A aplicação foi construída com foco em máxima portabilidade e zero complexidade de setup:
- **Linguagem:** Python 3.8 ou superior (disponível nativamente em Linux e macOS, instalável no Windows).
- **Dependências Externas:** Nenhuma dependência externa obrigatória para execução padrão (utiliza exclusivamente a biblioteca padrão do Python: `sqlite3`, `http.server`, `socketserver`, `json`, `urllib`).
- **Navegador:** Qualquer navegador web moderno com suporte a HTML5 e ES6+ (Google Chrome, Firefox, Edge, Safari, Opera).

---

## 3. Passo a Passo de Execução

### 3.1 Clonagem ou Acesso à Pasta do Projeto
Abra o terminal e navegue até a raiz do repositório:
```bash
cd /home/julio/pit-1_2
```

### 3.2 Inicialização do Servidor de Aplicação
Execute o script principal:
```bash
# No Linux ou macOS:
python3 server.py

# No Windows:
python server.py
```

O console exibirá a confirmação de inicialização:
```text
================================================================
 EquiTech ODS 5 - Portal MenHelpHer em execução!
 Projeto Integrado Transdisciplinar - Engenharia de Software
 Aluno: Julio Costa
 Banco de dados: /home/julio/pit-1_2/database/menhelpher.db
 Acesse no navegador: http://localhost:8000
================================================================
```

### 3.3 Acesso no Navegador
Abra o navegador e digite a URL:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 4. Variáveis de Ambiente Opcionais (Configuração Avançada)
É possível customizar o comportamento do servidor sem alterar código fonte definindo variáveis de ambiente:

| Variável | Padrão | Descrição |
|---|---|---|
| `MENHELPHER_HOST` | `127.0.0.1` | Interface de rede em que o servidor escutará |
| `MENHELPHER_PORT` | `8000` | Porta TCP do servidor web |
| `MENHELPHER_DB` | `database/menhelpher.db` | Caminho do arquivo de banco de dados SQLite |

Exemplo de execução em porta customizada:
```bash
MENHELPHER_PORT=8080 python3 server.py
```

---

## 5. Como Executar a Suíte de Testes Automatizados
O projeto conta com testes unitários, testes de integração RESTful e testes estáticos de integridade. Para rodar toda a suíte:

```bash
python3 -m unittest discover -s tests -t .
```

A saída esperada indicará a execução dos 56 testes automatizados com resultado `OK`:
```text
........................................................
----------------------------------------------------------------------
Ran 56 tests in ~12s

OK
```

Para testar o front-end via navegador (testes de unidade em JavaScript sem Node.js):
1. Inicie o servidor: `python3 server.py`
2. Abra no navegador: `http://localhost:8000/tests/frontend/runner.html` (ou execute via servidor estático na porta de testes).

---

## 6. Guia de Operação da Interface (Manual do Usuário)

### 6.1 Barra de Acessibilidade
Localizada no topo da tela:
- **🔊 Ler Tela:** Inicia ou interrompe a leitura automatizada em português do módulo ativo via síntese de voz nativa.
- **A+ / A / A-:** Aumenta, restaura ou reduz o tamanho tipográfico da aplicação (as preferências são salvas para as próximas visitas).
- **👁️ Alto Contraste:** Alterna para o modo de contraste reforçado para usuários com fotossensibilidade ou baixa visão.
- **☀️ Modo Claro / 🌙 Modo Escuro:** Altera o tema cromático geral.

### 6.2 Módulo 1: Painel de Indicadores
- Visualize os 4 KPIs principais com taxas de evasão e disparidade salarial oficial.
- Analise a visualização do funil de carreira e o gráfico circular de gap de remuneração.
- Estude a conexão entre as metas 5.1, 5.5 e 5.b da ONU com a rotina de squads de software.

### 6.3 Módulo 2: Simulador Gamificado
- Leia o cenário sociotécnico contextualizado (Code Review, Daily Scrum, Entrevista, Viés em IA, Avaliação de Desempenho).
- Escolha uma das alternativas de ação ética.
- Analise o feedback fundamentado no Código de Ética ACM/IEEE e confira as dicas práticas para aliados.
- Avance pelos 5 cenários para receber o diagnóstico e certificado digital de aliado da equidade.

### 6.4 Módulo 3: Mural HeForShe
- **Visualização:** Role pelo feed para ler compromissos registrados pela comunidade.
- **Filtros:** Clique nas pílulas de filtro (*Discentes*, *Docentes*, *Tech Leads*, *Engenheiros*) para segmentar os cards.
- **Apoio:** Clique em "❤️ Apoiar" para registrar seu endosso a um compromisso voluntário.
- **Novo Compromisso:** Preencha seu nome, selecione seu papel e o tipo de ação prática, redija sua declaração e clique em **"Publicar Compromisso no Mural"**.

### 6.5 Módulo 4: Pioneiras e Checklist
- Explore a trajetória histórica de Ada Lovelace, Margaret Hamilton, Grace Hopper e Claudia Bauzer Medeiros.
- Utilize o checklist de 6 pontos para auditar reuniões e repositórios do seu time.

### 6.6 Módulo 5: Avaliação de Impacto
- Avalie a clareza, relevância e absorção dos conceitos da plataforma em escala de 1 a 5.
- Deixe um comentário ou sugestão de melhoria.
- Observe a atualização imediata do quadro de **Métricas Consolidadas da Campanha**.

---

## 7. Documentação da API RESTful (Endpoints)

| Método | Endpoint | Descrição | Status de Sucesso |
|---|---|---|:---:|
| `GET` | `/api/saude` | Verificação de conectividade e integridade do banco | 200 OK |
| `GET` | `/api/metricas` | Totais de compromissos, apoios e médias das avaliações | 200 OK |
| `GET` | `/api/compromissos` | Listagem de todos os compromissos em ordem cronológica reversa | 200 OK |
| `POST` | `/api/compromissos` | Criação de novo compromisso comunitário | 201 Created |
| `POST` | `/api/compromissos/{id}/apoios` | Incremento de 1 apoio ao compromisso indicado | 200 OK |
| `GET` | `/api/avaliacoes` | Listagem das respostas do formulário de avaliação | 200 OK |
| `POST` | `/api/avaliacoes` | Registro de uma nova avaliação de impacto da campanha | 201 Created |
