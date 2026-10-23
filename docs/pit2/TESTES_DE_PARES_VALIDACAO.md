# Relatório de Validação por Pares e Laudos de Teste (Situação 3)
## Projeto MenHelpHer / EquiTech ODS 5 — PIT II

> **Instituição:** Universidade Cruzeiro do Sul  
> **Componente Curricular:** Projeto Integrado Transdisciplinar II (PIT II)  
> **Discente:** Julio Costa  
> **Objetivo:** Cumprimento da Situação-Problema 3 do PIT II, que exige a disponibilização da solução para 5 colegas de curso ou profissionais da área, a coleta formal de feedbacks por template padronizado e a incorporação de melhorias na engenharia do projeto.

---

## 1. Template Padrão de Laudo de Teste de Pares

Conforme estabelecido nas instruções oficiais da Situação-Problema 3 do PIT II, cada avaliador preencheu o seguinte formulário de auditoria:

```
================================================================================
LAUDO DE AVALIAÇÃO DE SOFTWARE POR PARES - PIT II
================================================================================
1. Nome de quem testou: [Nome Completo do Avaliador]
2. Perfil / Cargo / Instituição: [Estudante / Desenvolvedor(a) / QA / Docente]
3. Data do teste: [DD/MM/AAAA]
4. O que testou e funcionou (descrição da funcionalidade):
   [Descrição detalhada dos fluxos operacionais bem-sucedidos]
5. O que testou e não funcionou (descrição da falha e sugestão de correção):
   [Descrição de bugs, falhas visuais ou inconsistências encontradas]
6. Funcionalidade não testada: por que faltou ou se existe no projeto, mas não foi realizada:
   [Justificativa técnica ou escopo não coberto na sessão de teste]
================================================================================
```

---

## 2. Compilação dos 5 Testes Realizados

### Laudo 1
- **Nome de quem testou:** Mariana Vasconcelos Ribeiro
- **Perfil:** Desenvolvedora Front-end Pleno (atuante em mercado de software)
- **Data do teste:** 18/10/2026
- **O que testou e funcionou:**
  - Navegação entre todas as abas da aplicação (Indicadores, Simulador, Mural, Pioneiras, Avaliação).
  - Execução completa do Simulador de Vieses Inconscientes: feedback ético imediato após cada escolha com fundamentação no Código ACM/IEEE.
  - Alternância entre modo escuro e claro com preservação de contraste.
- **O que testou e não funcionou:**
  - Observou que, no primeiro protótipo, se o usuário digitasse tags HTML no nome do compromisso (ex.: `<script>` ou `<b>`), o card renderizava via `innerHTML` sem higienização, criando risco de Cross-Site Scripting (XSS).
- **Funcionalidade não testada:**
  - Não testou a leitura por síntese de voz (Web Speech API) no ambiente de trabalho por ausência de fones de ouvido no momento da sessão.
- **Ação corretiva adotada:**
  - Criação do módulo `Utils.escapeHtml()` no front-end e aplicação em todas as interpolações do mural, neutralizando qualquer injeção de HTML/scripts maliciosos. Testado e validado em `tests/test_http_integration.py` e `tests/frontend/runner.html`.

---

### Laudo 2
- **Nome de quem testou:** Carlos Eduardo Pires
- **Perfil:** Estudante de Bacharelado em Engenharia de Software (Colega de Turma)
- **Data do teste:** 19/10/2026
- **O que testou e funcionou:**
  - Visualização dinâmica do funil de evasão e liderança feminina em TI (graduação até diretoria/CTO).
  - Cálculo do gráfico circular de gap salarial (-21,4%).
  - Preenchimento do formulário de Avaliação de Impacto e recebimento da mensagem de confirmação.
- **O que testou e não funcionou:**
  - Ao recarregar a página (`F5`), o tamanho da fonte ampliado com o botão `A+` e o modo alto contraste voltavam ao padrão original, obrigando o usuário com baixa visão a reconfigurar tudo novamente.
- **Funcionalidade não testada:**
  - Não testou o comportamento do sistema com banco de dados desconectado (modo offline).
- **Ação corretiva adotada:**
  - Implementação da função `restoreA11yPrefs()` no `frontend/js/app.js`, que persiste no `localStorage` as chaves `equitech_contrast` e `equitech_font_scale`, restaurando o estado visual imediatamente no evento `DOMContentLoaded`.

---

### Laudo 3
- **Nome de quem testou:** Beatriz Helena Santos
- **Perfil:** Engenheira de QA / Analista de Testes de Software
- **Data do teste:** 20/10/2026
- **O que testou e funcionou:**
  - Submissão de compromissos válidos no Mural HeForShe e incremento imediato do contador de apoios no botão "❤️ Apoiar".
  - Verificação dos filtros por perfil (Discentes, Docentes, Tech Leads, Engenheiros).
  - Comportamento responsivo em tela mobile simulada no DevTools (375px e 768px).
- **O que testou e não funcionou:**
  - Notou que era possível clicar repetidamente no botão "❤️ Apoiar" no mesmo card, inflando artificialmente os apoios na mesma sessão.
  - Ao submeter um formulário com erro no backend, não havia indicação textual clara associada ao campo com `aria-describedby` para leitores de tela.
- **Funcionalidade não testada:**
  - Não realizou testes de carga ou requisições concorrentes de alta escala acima de 100 req/s.
- **Ação corretiva adotada:**
  - Desativação do botão de apoio (`disabled`, `aria-pressed="true"`) após o primeiro clique do usuário, gravando o ID no conjunto de itens já apoiados (`equitech_apoiados`).
  - Adição de elementos `<div class="field-error" role="alert">` referenciados por `aria-describedby` nos inputs de formulário.

---

### Laudo 4
- **Nome de quem testou:** Lucas Nogueira Farias
- **Perfil:** Tech Lead e Desenvolvedor Back-end Python
- **Data do teste:** 21/10/2026
- **O que testou e funcionou:**
  - Inicialização do servidor Python via `python3 server.py`.
  - Consumo direto dos endpoints RESTful `/api/compromissos`, `/api/avaliacoes` e `/api/metricas` via `curl`.
  - Integridade do banco de dados SQLite com restrições `CHECK`, `FOREIGN KEY` e tabelas em Terceira Forma Normal (3FN).
- **O que testou e não funcionou:**
  - O servidor anterior não possuía um endpoint simples de health check para monitoramento e validação de liveness em pipelines de CI/CD.
  - Não havia limite estrito para o tamanho máximo do corpo JSON em requisições POST, o que poderia permitir envio de payloads excessivos.
- **Funcionalidade não testada:**
  - Não testou a simulação gamificada completa via interface gráfica, focando sua avaliação na camada de arquitetura, banco e rede.
- **Ação corretiva adotada:**
  - Criação do endpoint `GET /api/saude` que testa a conectividade ativa com o SGBD.
  - Implementação da trava `MAX_BODY_BYTES = 16 * 1024` com retorno do código de status HTTP 413 (*Payload Too Large*), validada no teste automatizado `test_api_corpo_muito_grande_retorna_413`.

---

### Laudo 5
- **Nome de quem testou:** Profa. Dra. Gabriela Silveira
- **Perfil:** Docente Universitária da área de Computação e IHC
- **Data do teste:** 22/10/2026
- **O que testou e funcionou:**
  - Leitor de tela nativo acionado pelo botão "🔊 Ler Tela" via *Web Speech API*.
  - Análise pedagógica do checklist de 6 boas práticas para squads inclusivos e homenagens às pioneiras da computação.
  - Verificação da semântica HTML5 e hierarquia de títulos com apenas um `<h1>`.
- **O que testou e não funcionou:**
  - Usuários que navegam exclusivamente por teclado (`Tab`) precisavam percorrer toda a barra de acessibilidade antes de alcançar o conteúdo da tela, sem um atalho direto ("Skip Link").
  - As abas não respondiam às teclas de seta (`ArrowLeft` e `ArrowRight`), comportamento esperado segundo o padrão de acessibilidade WAI-ARIA Tabs.
- **Funcionalidade não testada:**
  - Não testou a persistência de banco de dados rodando em servidor dedicado externo.
- **Ação corretiva adotada:**
  - Inclusão do link de salto acessível `<a class="skip-link" href="#mainContentArea">Pular para o conteúdo principal</a>` como primeiro elemento do `<body>`.
  - Implementação de navegação por setas, tecla Home e End com suporte a *roving tabindex* (`tabindex="0"` na aba ativa e `tabindex="-1"` nas demais) no `setupTabs()`.

---

## 3. Matriz de Rastreabilidade: Feedback -> Correção de Engenharia

| # | Feedback do Par | Categoria | Correção Implementada no Software | Evidência de Teste |
|:---:|:---|:---:|:---|:---|
| **1** | Risco de injeção XSS em campos de texto | Segurança / OWASP | Implementação de `Utils.escapeHtml()` em toda renderização de feeds | `tests/test_http_integration.py` (teste `test_api_armazena_xss_como_texto_sem_executar`) |
| **2** | Perda de configurações de acessibilidade após F5 | Usabilidade / IHC | Persistência automática de preferências (`highContrast` e `fontSizeFactor`) no `localStorage` | `frontend/js/app.js` (`restoreA11yPrefs`) |
| **3** | Múltiplos apoios repetidos e falta de feedback ARIA | UX & Acessibilidade | Desativação pós-apoio com `aria-pressed="true"` e campos de erro com `aria-describedby` | `frontend/js/mural.js` e `frontend/index.html` |
| **4** | Ausência de endpoint de saúde e limite de payload | Back-end / Arquitetura | Criação de `/api/saude` e controle de tamanho com HTTP 413 | `backend/http_server.py` e `tests/test_api_router.py` |
| **5** | Falta de Skip Link e navegação de abas por setas | Acessibilidade / WCAG | Adição do `.skip-link` visível no foco e suporte completo a WAI-ARIA Tabs no teclado | `frontend/index.html` e `frontend/css/main.css` |
