# Roteiro de Gravação do Vídeo de Apresentação (Até 5 Minutos)
## MenHelpHer / EquiTech ODS 5 — Conclusão PIT II

> **Instituição:** Universidade Cruzeiro do Sul  
> **Componente Curricular:** Projeto Integrado Transdisciplinar II (PIT II)  
> **Discente:** Julio Costa  
> **Tempo Total Alvo:** Entre 4 minutos e 30 segundos e 5 minutos (rigorosamente dentro do limite acadêmico de até 5 minutos).  
> **Formato de Entrega:** Vídeo narrado com captura de tela da aplicação em funcionamento local (`http://localhost:8000`).

---

## 1. Instruções Prévias para o Discente
1. **Ambiente:** Certifique-se de que o servidor está em execução (`python3 server.py`) e abra o navegador em `http://localhost:8000`.
2. **Resolução de Tela:** Recomendado gravar em 1080p (Full HD - 1920x1080) com zoom padrão do navegador em 100%.
3. **Áudio:** Falar com clareza, ritmo moderado e tom seguro de engenheiro(a) de software.

---

## 2. Cronograma Minuto a Minuto da Apresentação

### Bloco 1: Abertura, Contexto Acadêmico e ODS 5 (0:00 a 0:45)
- **O que mostrar na tela:** Página inicial da plataforma (`http://localhost:8000`), destacando a barra superior de identificação acadêmica e a seção Hero.
- **Fala sugerida:**
  > *"Olá, professores, tutores e colegas da Universidade Cruzeiro do Sul! Meu nome é Julio Costa, discente de Engenharia de Software, e estou aqui para apresentar a conclusão do meu Projeto Integrado Transdisciplinar II (PIT II), a plataforma MenHelpHer / EquiTech ODS 5.*  
  > *Este projeto iniciou no PIT I, onde planejamos e prototipamos uma solução sociotécnica focada no Objetivo de Desenvolvimento Sustentável 5 da ONU, combatendo vieses inconscientes e a sub-representação feminina em tecnologia com apoio do Programa Meninas Digitais da SBC e da campanha HeForShe da ONU Mulheres.*  
  > *Agora, no PIT II, evoluímos a solução para uma arquitetura profissional Model-View-Controller (MVC) com SGBD relacional, suíte de testes automatizados e validação com pares."*

---

### Bloco 2: Painel de Indicadores e Recursos de Acessibilidade (0:45 a 1:40)
- **O que mostrar na tela:**
  - Alternar modo alto contraste no topo e demonstrar o botão "A+" de zoom de fonte.
  - Clicar brevemente em "🔊 Ler Tela" para ouvir a síntese de voz nativa.
  - Rolar pelo Painel de Indicadores mostrando os dados da SBC, o Funil de Liderança e o gráfico do Gap Salarial (-21,4%).
- **Fala sugerida:**
  > *"No primeiro módulo, temos o Painel de Indicadores Oficiais, embasado em dados abertos do IPEA, SBC e Inep. Podemos visualizar o funil de carreira — onde a presença feminina cai de 18% no ingresso universitário para apenas 9% em cargos de CTO e diretoria — e a disparidade salarial de 21,4% em funções equivalentes.*  
  > *A aplicação foi desenvolvida sob rigorosos padrões de acessibilidade WCAG: conta com alternador dinâmico de tema claro e escuro, modo de alto contraste para fotossensibilidade, redimensionamento de fontes persistido localmente e síntese de voz nativa para pessoas com deficiência visual."*

---

### Bloco 3: Simulador Gamificado de Vieses Inconscientes (1:40 a 2:40)
- **O que mostrar na tela:** Clicar na aba "🎮 Simulador de Vieses Inconscientes", resolver o primeiro cenário de Code Review escolhendo a opção exemplar e depois avançar um cenário.
- **Fala sugerida:**
  > *"O segundo módulo é o Simulador Gamificado de Vieses Inconscientes. Ele coloca o discente ou engenheiro diante de situações reais do cotidiano de equipes ágeis, como revisões de código no GitHub, reuniões de arquitetura com interrupções de fala e processos seletivos.*  
  > *Ao responder, o usuário não recebe apenas uma pontuação, mas um feedback imediato com fundamentação ética baseada no Código de Ética do IEEE e ACM, além de dicas práticas para se tornar um aliado proativo no squad. Ao final dos 5 cenários, a plataforma gera uma certificação digital de aliado da equidade."*

---

### Bloco 4: Mural HeForShe, SGBD Relacional e Persistência (2:40 a 3:45)
- **O que mostrar na tela:**
  - Clicar na aba "🤝 Mural HeForShe".
  - Mostrar os cartões carregados diretamente do banco de dados SQLite.
  - Clicar no botão "❤️ Apoiar" de um cartão (mostrar incremento e desativação do botão).
  - Preencher e enviar um novo compromisso (ex.: Nome: "Julio Costa", Papel: "Estudante", Ação: "Code Review Inclusivo", Mensagem: "Comprometo-me a acolher e apoiar colegas mulheres em arquitetura.").
  - Mostrar o card publicado no topo imediatamente.
- **Fala sugerida:**
  > *"No Mural de Compromissos HeForShe, qualquer membro da comunidade acadêmica pode assinar publicamente uma postura ética. Aqui temos uma grande inovação técnica do PIT II: a migração de arquivos locais para um banco de dados relacional SQLite padronizado em 3ª Forma Normal, com integridade referencial e validações estritas.*  
  > *Ao clicar em apoiar, a requisição consome nossa API RESTful via endpoint `/api/compromissos/{id}/apoios`. Ao publicar um novo compromisso, os dados são sanitizados contra vulnerabilidades como XSS e gravados no banco. Caso o servidor esteja offline, o sistema possui resiliência automática com fallback para LocalStorage."*

---

### Bloco 5: Avaliação de Impacto, Testes e Encerramento (3:45 a 5:00)
- **O que mostrar na tela:**
  - Clicar na aba "📝 Avaliação de Impacto", enviar uma avaliação e destacar o painel dinâmico de "Métricas Consolidadas da Campanha".
  - Alternar rapidamente para o terminal e executar o comando de testes: `python3 -m unittest discover -s tests -t .`, mostrando os 106 testes passando em verde com 100% de cobertura backend.
- **Fala sugerida:**
  > *"Na última aba, temos a Avaliação de Impacto da Campanha, correspondente à Etapa 5 do projeto. As notas submetidas alimentam em tempo real o painel de métricas consolidadas através do nosso Controller de Métricas.*  
  > *Para comprovar a excelência de engenharia exigida na Situação 3 do PIT II, desenvolvemos uma suíte com 106 testes automatizados que cobrem modelos de domínio, controllers com mocks, views de serialização, rotas RESTful, integridade estática e integração HTTP real com 100% de cobertura de código no backend. Além disso, submetemos o sistema a 5 avaliadores e dublês de usuário, cujos laudos resultaram em melhorias cruciais como proteção XSS e navegação completa por teclado.*  
  > *Desta forma, encerramos com êxito o ciclo entre PIT I e PIT II, entregando um artefato sociotécnico completo, seguro e com impacto social direto. Muito obrigado a todos!"*
