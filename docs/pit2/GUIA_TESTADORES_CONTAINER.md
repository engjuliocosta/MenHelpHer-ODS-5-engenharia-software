# 🐳 Guia de Execução em Contêiner para Avaliadores e Testadores (PIT II)
## MenHelpHer / EquiTech ODS 5 — Plataforma de Equidade de Gênero na Engenharia de Software

> **Instituição de Ensino Superior:** Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)  
> **Curso:** Bacharelado em Engenharia de Software  
> **Discente / Autor:** Julio Costa  
> **Projeto:** Projeto Integrado Transdisciplinar (PIT I e PIT II)  
> **Versão da Imagem:** `menhelpher:latest` (Docker Engine / Docker Compose)

---

## 🎯 Objetivo Deste Guia

Este documento orienta avaliadores acadêmicos, tutores, docentes e pares (dublês de usuário) a **executar e testar a aplicação de ponta a ponta com um único comando**, de forma 100% automatizada e dinâmica, sem necessidade de configurar previamente interpretadores Python, criar ambientes virtuais (`venv`) ou instalar dependências manuais na máquina de testes.

Todo o ecossistema (servidor HTTP nativo MVC, banco relacional SQLite 3 com catálogo e dados de demonstração, front-end responsivo e suíte completa de 106 testes automatizados) é provisionado dentro de um contêiner Docker seguro e isolado.

---

## ⚡ Como Executar com 1 Comando (Zero Atrito)

### No Linux, macOS ou Windows via WSL:
Abra o terminal na pasta raiz do projeto e execute:

```bash
./executar_container.sh
```

### No Windows (Prompt de Comando ou PowerShell):
Dê um duplo clique no arquivo [`executar_container.bat`](file:///home/julio/pit-1_2/executar_container.bat) ou execute no CMD:

```cmd
executar_container.bat
```

---

## 🤖 O que o Script Dinâmico Faz Automaticamente

O script foi projetado para resolver todos os passos sem intervenções repetitivas:

1. **Detecção e Instalação do Docker:**  
   Verifica se o comando `docker` está disponível. No Linux (Ubuntu/Debian), caso não esteja instalado, o script oferece a instalação assistida do Docker oficial em uma única confirmação.
2. **Ativação do Daemon:**  
   Se o serviço Docker estiver desligado, o script tenta iniciá-lo automaticamente (`systemctl` / `service`).
3. **Resolução de Conflitos de Porta:**  
   Garante que a porta `8000` esteja livre para o contêiner.
4. **Construção e Orquestração (`docker compose`):**  
   Compila a imagem baseada em `python:3.12-slim`, configura o usuário seguro não-root (`appuser`), monta o volume do banco de dados relacional e sobe o contêiner em modo *detached*.
5. **Monitoramento Ativo de Saúde (*Healthcheck*):**  
   Aguarda a resposta positiva do endpoint `GET /api/saude`.
6. **Abertura Automática do Navegador:**  
   Detecta o navegador padrão do sistema operacional e abre automaticamente a URL:  
   👉 **[http://localhost:8000](http://localhost:8000)**
7. **Menu Interativo do Testador no Terminal:**  
   Mantém um console interativo para o testador com as seguintes opções:
   - `[1]` Reabrir a interface no navegador.
   - `[2]` **Executar a suíte de 106 testes unitários com cobertura de 100% dentro do contêiner**.
   - `[3]` Monitorar logs do servidor HTTP em tempo real.
   - `[4]` Resetar o banco de dados para os valores padrão de demonstração.
   - `[5]` Encerrar o contêiner e limpar a rede.

---

## 📋 Roteiro de Testes Recomendados para o Avaliador

| Etapa | Funcionalidade a Testar | O que observar | Critério de Aceitação |
| :---: | :--- | :--- | :--- |
| **1** | **Barra de Acessibilidade (Topo)** | Clique em "🔊 Ler Tela", "A+", "A-", "👁️ Alto Contraste" e tema Claro/Escuro. | Leitura em voz audível no navegador, ajuste instantâneo da escala de texto e contraste reforçado com persistência. |
| **2** | **Módulo 1: Painel de Indicadores** | Visualizar cards de KPI, gráfico de funil de retenção e conexão com as metas 5.1, 5.5 e 5.b da ONU. | Layout fluido, ausência de quebras visuais e números estatísticos fidedignos. |
| **3** | **Módulo 2: Guia de Ação e Vieses** | Explorar os cards de vieses inconscientes (Efeito Matilda, Prova Dupla) e checklist prático. | Textos claros, informativos e fundamentados nas diretrizes da SBC. |
| **4** | **Módulo 3: Simulação Gamificada** | Selecionar um dos 3 cenários práticos (Code Review, Contratação ou Promoção) e escolher uma resposta. | Feedback pedagógico imediato explicando o impacto da decisão na retenção feminina. |
| **5** | **Módulo 4: Mural de Compromissos** | Preencher o formulário, selecionar seu papel na TI, enviar e clicar no botão "Apoiar (+1)". | Validação em tempo real, inclusão instantânea no feed e incremento do contador persistido no SQLite. |
| **6** | **Módulo 5: Avaliação de Impacto** | Preencher as notas de 1 a 5 nas 3 dimensões (clareza, vieses, relevância ODS 5) e submeter. | Exibição de mensagem de sucesso e atualização imediata do painel de **Métricas Consolidadas**. |
| **7** | **Segurança e Validação (Anti-XSS)** | Tentar inserir `<script>alert(1)</script>` no campo nome ou mensagem do compromisso. | O texto é sanitizado defensivamente via `Utils.escapeHtml()` sem execução de código malicioso. |
| **8** | **Suíte Automatizada de Testes** | Pressionar a opção `[2]` no menu do terminal ou executar o comando de teste no contêiner. | **106 testes aprovados com 100% de cobertura** no backend. |

---

## 💻 Comandos Manuais do Docker (Opcional)

Caso prefira operar via CLI nativa do Docker sem os scripts interativos:

### Iniciar o contêiner:
```bash
docker compose up -d --build
```

### Visualizar status e saúde:
```bash
docker compose ps
```

### Executar a suíte de testes com relatório de cobertura no contêiner:
```bash
docker compose exec menhelpher pytest --cov=backend --cov-report=term-missing
```

### Executar via `unittest` padrão dentro do contêiner:
```bash
docker compose exec menhelpher python3 -m unittest discover -s tests -t .
```

### Testar a API RESTful diretamente via `curl`:
```bash
# Verificação de saúde da aplicação e conectividade com o SGBD
curl -i http://localhost:8000/api/saude

# Consulta de métricas agregadas da campanha
curl -i http://localhost:8000/api/metricas

# Listagem de compromissos
curl -i http://localhost:8000/api/compromissos
```

### Parar o contêiner:
```bash
docker compose down
```

---

## 📝 Template de Feedback do Avaliador (Dublê de Usuário)

Caso você esteja participando como avaliador de pares para a disciplina PIT II, preencha o formulário abaixo e envie ao discente Julio Costa para inclusão no documento de validação:

```markdown
### Laudo de Avaliação do Contêiner
- **Nome do(a) Avaliador(a):** [Seu Nome Completo]
- **Perfil Profissional / Acadêmico:** [Ex: Desenvolvedor(a), Estudante de TI, Tech Lead, etc.]
- **Data do Teste:** [DD/MM/AAAA]
- **Ambiente de Teste:** [Ex: Ubuntu 24.04 / Windows 11 / macOS com Docker Desktop]
- **O que testou e funcionou:**
  - [Descrever facilidade de execução com o script]
  - [Descrever usabilidade da interface, acessibilidade e envio de dados]
- **O que testou e encontrou como oportunidade de melhoria:**
  - [Descrever sugestões de melhoria técnica ou de experiência do usuário]
- **Avaliação Geral da Aplicação (Notas de 1 a 5):**
  - Clareza da Proposta: [ ]
  - Facilidade de Execução via Contêiner: [ ]
  - Relevância para o ODS 5 na Engenharia de Software: [ ]
```

---

## 🏛️ Dados Acadêmicos Oficiais
- **Instituição:** Universidade Cruzeiro do Sul (Cruzeiro do Sul Virtual)
- **Discente:** Julio Costa
- **Curso:** Bacharelado em Engenharia de Software
- **Disciplinas:** Projeto Integrado Transdisciplinar I e II (PIT I e PIT II)
- **Ano:** 2026
