# MenHelpHer
## Plataforma de Sensibilização e Equidade de Gênero na Engenharia de Software

> **Projeto Integrado Transdisciplinar (PIT I)**  
> **Curso:** Bacharelado em Engenharia de Software  
> **Autor / Discente:** Julio Costa  
> **Tema Central:** ODS 5 da ONU (Metas 5.1, 5.5 e 5.b da Agenda 2030)  
> **Metodologia:** Design Thinking + Scrum Híbrido  
> **Alinhamento:** Programa Meninas Digitais (SBC) & Movimento HeForShe / ElesPorElas (ONU Mulheres)

---

## 🌟 Visão Geral

A **EquiTech ODS 5** é uma aplicação web interativa e acessível (Mobile-First) projetada para combater a sub-representação feminina e os vieses inconscientes na Engenharia de Software e no setor de Tecnologia da Informação (TI).

O projeto une rigor científico, responsabilidade social e excelência técnica, demonstrando que o desenvolvimento de software é uma **atividade sociotécnica** orientada pela ética profissional (Código de Ética ACM/IEEE).

---

## 🚀 Módulos da Aplicação

### 1. 📊 Painel de Indicadores e Dados (Data Dashboard)
- Curadoria de indicadores oficiais da **SBC (Sociedade Brasileira de Computação)**, **IPEA (Retrato das Desigualdades)**, **Inep/MEC** e **ONU Mulheres**.
- **Métricas Chave**:
  - `15,2%`: Participação feminina em cursos de graduação em computação no Brasil (queda de 70% em relação aos anos 80).
  - `17,8%`: Mulheres no mercado de trabalho em funções técnicas de TI.
  - `13,6%`: Mulheres em posições de liderança técnica (CTOs, VPs de Engenharia, Tech Leads).
  - `21,4%`: Disparidade salarial média em cargos técnicos equivalentes de desenvolvimento.
- Visualização dinâmica do **Funil de Evasão e Liderança em Computação**.
- Metas **5.1**, **5.5** e **5.b** da Agenda 2030 traduzidas para a prática de squads ágeis.

### 2. 🎮 Simulador Gamificado de Vieses Inconscientes
- 5 cenários práticos e realistas contextualizados na rotina de equipes de tecnologia:
  1. **Code Review com Exigências Desproporcionais** (*Prove-it-again bias* no GitHub/GitLab).
  2. **Daily Scrum e 'Manterrupting' em Arquitetura** (Interrupções de fala e apropriação de ideias).
  3. **Entrevista Técnica & Viés de Ajuste Cultural** (Perguntas invasivas e discriminação familiar).
  4. **Viés Algorítmico & Ética em IA no Hackathon** (*Sampling bias* e algoritmos discriminatórios).
  5. **Avaliação 360 & Duplo Padrão de Liderança** (Julgamento comportamental e promoção para Staff Engineer).
- Feedback imediato com pontuação, explicação fundamentada no **Código ACM/IEEE** e dicas práticas para aliados da equidade.

### 3. 🤝 Mural Digital de Compromissos (Inspirado no HeForShe / ElesPorElas)
- Registro público e voluntário de compromissos individuais por discentes, docentes e profissionais de TI.
- Categorias de compromisso:
  - *Revisão de Código Inclusiva e Respeitosa*
  - *Combate ao Manterrupting em Reuniões*
  - *Mentoria Ativa para Mulheres em Computação*
  - *Fomento a Lideranças Femininas*
  - *Defesa de Paridade Salarial e Oportunidades Justas*
- Feed dinâmico com contadores de apoio (curtidas), filtros por perfil e persistência de dados.

### 4. 📚 Pioneiras Históricas & Checklist para Squads
- Biografias e legados de **Ada Lovelace**, **Margaret Hamilton**, **Grace Hopper** e da cientista brasileira **Claudia Bauzer Medeiros**.
- **Checklist de 6 Boas Práticas** para squads e laboratórios acadêmicos inclusivos.
- Conexões diretas com o **Programa Meninas Digitais (SBC)** e **HeForShe**.

### 5. 📝 Avaliação de Impacto da Campanha
- Formulário eletrônico integrado para mensurar a clareza, relevância e absorção de conceitos pelos participantes (Etapa 5 do PIT).

---

## ♿ Recursos de Acessibilidade (WCAG)

- **Modo Alto Contraste**: Adaptado para pessoas com baixa visão ou fotossensibilidade.
- **Redimensionamento de Fonte Dinâmico** (`A+`, `A`, `A-`).
- **Leitor de Tela Nativo**: Síntese de voz em português via *Web Speech API*.
- **Alternador de Tema**: Modo Escuro (*Dark Mode*) e Modo Claro (*Light Mode*).
- **Semântica HTML5 e ARIA**: Totalmente navegável por teclado (`Tab`, `:focus-visible`).

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5 Semântico, Vanilla CSS Moderno (Design Tokens, Glassmorphism, CSS Custom Properties), JavaScript ES6+ Modular.
- **Backend**: Python 3 nativo (`http.server` com API RESTful JSON para gravação de compromissos, avaliações e métricas).
- **Armazenamento**: `data/compromissos.json` e `data/avaliacoes.json` com fallback para `localStorage`.

---

## 💻 Como Executar e Testar Localmente

A aplicação foi desenvolvida sem dependências externas pesadas (sem necessidade de `npm install` ou pacotes externos via `pip`), garantindo execução imediata e leve.

### 📋 Pré-requisitos
- **Python 3.x** instalado (disponível por padrão no Linux/macOS ou facilmente instalado no Windows).
- Qualquer navegador web moderno (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari).

---

### 🚀 Passo a Passo Rápido

#### 1. Abra o terminal na pasta do projeto:
```bash
cd /home/julio/pit-1_2
```

#### 2. Inicie o servidor integrado:
```bash
# No Linux / macOS:
python3 server.py

# No Windows:
python server.py
```
> O terminal exibirá a mensagem de confirmação:  
> `EquiTech ODS 5 - Portal MenHelpHer em execução!`  
> `Acesse no navegador: http://localhost:8000`

#### 3. Acesse a aplicação:
Abra seu navegador e entre no link:  
👉 **[http://localhost:8000](http://localhost:8000)**

---

### 🧪 Roteiro de Testes Recomendado (O que validar na plataforma)

Para comprovar o funcionamento de todos os módulos avaliados no PIT I, siga este roteiro de testes:

1. **Acessibilidade & Usabilidade (Topo da Página):**
   - Clique em **"👁️ Alto Contraste"** para alternar o modo de acessibilidade visual.
   - Use os botões **"A+"**, **"A-"** e **"A"** para testar o redimensionamento dinâmico de fonte.
   - Clique em **"🔊 Ler Tela"** para ouvir a leitura do conteúdo ativo via síntese de voz nativa (*Web Speech API*).
   - Alterne entre **"☀️ Modo Claro"** e **"🌙 Modo Escuro"**.

2. **📊 Teste do Painel de Indicadores (Aba 1):**
   - Visualize os cards de dados oficiais da SBC e IPEA.
   - Observe a animação do **Funil de Carreira em Computação** (da graduação até CTO).
   - Verifique o gráfico circular de **Gap Salarial** (-21,4%).
   - Leia a aplicação prática das metas **5.1**, **5.5** e **5.b** da Agenda 2030 na rotina de squads.

3. **🎮 Teste do Simulador de Vieses Inconscientes (Aba 2):**
   - Leia o primeiro cenário de **Code Review no GitHub** e selecione uma das opções.
   - Observe o feedback imediato com a explicação ética fundamentada no **Código ACM/IEEE** e a atualização da pontuação.
   - Avance até o fim dos 5 cenários para receber a classificação final e o badge de *"Aliado(a) da Equidade"*.

4. **🤝 Teste do Mural HeForShe (Aba 3):**
   - Clique no botão **"❤️ Apoiar"** em qualquer cartão de compromisso e veja o contador aumentar instantaneamente.
   - Use os filtros no topo do feed (*Discentes*, *Docentes*, *Tech Leads*, *Engenheiros*) para filtrar os cards.
   - Preencha o formulário à esquerda com seu nome, papel e mensagem e clique em **"Publicar Compromisso no Mural"**. Seu compromisso aparecerá imediatamente no feed e será gravado no arquivo `data/compromissos.json`.

5. **📝 Teste da Avaliação de Impacto (Aba 5):**
   - Preencha o formulário de feedback da semana de sensibilização e envie para validar a persistência em `data/avaliacoes.json`.

---

### 🌐 Opção de Teste Direto (Sem Terminal)
Caso prefira não utilizar a linha de comando, basta dar um duplo clique diretamente no arquivo [`index.html`](file:///home/julio/pit-1_2/index.html) para abri-lo no seu navegador padrão. A aplicação funcionará com todos os recursos e armazenamento local (*LocalStorage*).

---

## 📁 Estrutura de Diretórios

```
pit-1_2/
├── index.html                           # Interface web principal da plataforma
├── server.py                            # Servidor Python com API RESTful
├── README.md                            # Documentação geral do projeto
├── css/
│   ├── main.css                         # Design system, tokens, acessibilidade e temas
│   ├── dashboard.css                    # Estilos dos KPIs e funil de liderança
│   ├── simulator.css                    # Estilos da gamificação e cenários
│   └── mural.css                        # Estilos do mural HeForShe e formulários
├── js/
│   ├── app.js                           # Controlador geral e acessibilidade
│   ├── data.js                          # Base de dados estatísticos oficiais
│   ├── dashboard.js                     # Renderização de indicadores e gráficos
│   ├── simulator.js                     # Mecânica e feedback do quiz de vieses
│   └── mural.js                         # Lógica do mural de compromissos e avaliação
├── data/
│   ├── compromissos.json                # Registros de compromissos comunitários
│   └── avaliacoes.json                  # Respostas da avaliação de impacto
└── docs/
    ├── PROJETO_PIT_APRESENTACAO.md      # Relatório acadêmico completo do PIT I
    └── CARTAZ_CAMPANHA_DIVULGACAO.md    # Material de divulgação e cartaz com QR Code
```

---

## 📜 Autor e Informações Acadêmicas

- **Discente:** Julio Costa
- **Curso:** Engenharia de Software
- **Componente Curricular:** Projeto Integrado Transdisciplinar I (PIT I)
- **Ano:** 2026
