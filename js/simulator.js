/**
 * MenHelpHer - Lógica do Simulador Gamificado de Situações Reais
 * Autor: Julio Costa
 */

const SimulatorModule = {
  currentScenarioIndex: 0,
  score: 0,
  userAnswers: [],

  init() {
    this.currentScenarioIndex = 0;
    this.score = 0;
    this.userAnswers = [];
    this.renderCurrentScenario();
  },

  renderCurrentScenario() {
    const container = document.getElementById('simulatorView');
    if (!container) return;

    const totalScenarios = EQUI_DATA.cenariosSimulador.length;

    // Se concluiu todos os cenários
    if (this.currentScenarioIndex >= totalScenarios) {
      this.renderCompletionScreen(container);
      return;
    }

    const scenario = EQUI_DATA.cenariosSimulador[this.currentScenarioIndex];
    const progressPercent = Math.round(((this.currentScenarioIndex + 1) / totalScenarios) * 100);

    container.innerHTML = `
      <div class="simulator-header">
        <div class="sim-progress-box">
          <div class="sim-progress-label">
            <span>Cenário ${this.currentScenarioIndex + 1} de ${totalScenarios}</span>
            <span>${progressPercent}% Concluído</span>
          </div>
          <div class="sim-progress-track">
            <div class="sim-progress-fill" style="width: ${progressPercent}%;"></div>
          </div>
        </div>
        <div class="sim-score-badge">
          <span class="score-icon">⭐</span>
          <div>
            <div class="score-val">${this.score} pts</div>
            <div class="score-lbl">Score de Aliado</div>
          </div>
        </div>
      </div>

      <div class="scenario-card" id="activeScenarioCard">
        <div class="scenario-category">🎯 ${scenario.categoria}</div>
        <h2 class="scenario-title">${scenario.titulo}</h2>
        
        <div class="scenario-context-box">
          <div class="ide-header">
            <span class="ide-dot dot-red"></span>
            <span class="ide-dot dot-yellow"></span>
            <span class="ide-dot dot-green"></span>
            <span style="margin-left: 0.5rem;">squad_daily_and_code_review.log — Simulação Sociotécnica</span>
          </div>
          <p>${scenario.situacao}</p>
        </div>

        <div class="scenario-question">🤔 ${scenario.pergunta}</div>

        <div class="options-list" id="optionsList">
          ${scenario.opcoes.map(opcao => `
            <button class="option-btn" onclick="SimulatorModule.handleChoice('${opcao.id}')" id="btn-opt-${opcao.id}">
              <span class="option-letter">${opcao.id}</span>
              <span class="option-text">${opcao.texto}</span>
            </button>
          `).join('')}
        </div>

        <div class="feedback-box" id="feedbackBox">
          <div class="feedback-title" id="feedbackTitle"></div>
          <div id="feedbackText"></div>
          <div class="feedback-ethics" id="feedbackEthics">
            <strong>Fundamentação Ética & Regulamentar:</strong>
            <p>${scenario.fundamentacaoEtica}</p>
          </div>
          <div class="feedback-tip" id="feedbackTip">
            💡 <strong>Dica Prática para Aliados:</strong> ${scenario.dicaAliado}
          </div>
          <div class="sim-actions">
            <button class="btn btn-primary" onclick="SimulatorModule.nextScenario()">
              ${this.currentScenarioIndex + 1 < totalScenarios ? 'Próximo Cenário ➔' : 'Ver Meu Diagnóstico Final 🏆'}
            </button>
          </div>
        </div>
      </div>
    `;
  },

  handleChoice(optionId) {
    const scenario = EQUI_DATA.cenariosSimulador[this.currentScenarioIndex];
    const selectedOption = scenario.opcoes.find(o => o.id === optionId);
    if (!selectedOption) return;

    // Desabilitar botões
    const allButtons = document.querySelectorAll('.option-btn');
    allButtons.forEach(btn => btn.disabled = true);

    // Atualizar pontuação
    this.score += selectedOption.pontos;
    this.userAnswers.push({
      scenarioId: scenario.id,
      selectedOption: optionId,
      points: selectedOption.pontos
    });

    // Atualizar visual do botão clicado
    const selectedBtn = document.getElementById(`btn-opt-${optionId}`);
    if (selectedOption.pontos >= 8) {
      selectedBtn.classList.add('selected-correct');
    } else if (selectedOption.pontos <= 0) {
      selectedBtn.classList.add('selected-wrong');
    } else {
      selectedBtn.classList.add('selected-partial');
    }

    // Exibir caixa de feedback
    const feedbackBox = document.getElementById('feedbackBox');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const feedbackText = document.getElementById('feedbackText');

    feedbackBox.classList.remove('correto', 'alerta', 'erro');

    if (selectedOption.pontos >= 8) {
      feedbackBox.classList.add('correto');
      feedbackTitle.innerHTML = '✅ Decisão Inclusiva e Exemplar!';
    } else if (selectedOption.pontos > 0) {
      feedbackBox.classList.add('alerta');
      feedbackTitle.innerHTML = '⚠️ Boa intenção, mas requer cuidado de processo';
    } else {
      feedbackBox.classList.add('erro');
      feedbackTitle.innerHTML = '❌ Atenção: Esta postura reforça o viés inconsciente';
    }

    feedbackText.innerHTML = `<p>${selectedOption.feedback}</p>`;
    feedbackBox.classList.add('active');

    // Scroll suave para o feedback
    feedbackBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },

  nextScenario() {
    this.currentScenarioIndex++;
    this.renderCurrentScenario();
    window.scrollTo({ top: document.getElementById('simulatorView').offsetTop - 90, behavior: 'smooth' });
  },

  renderCompletionScreen(container) {
    const maxScore = EQUI_DATA.cenariosSimulador.length * 10;
    let badgeTitle = "Engenheiro(a) Aliado(a) da Equidade ODS 5";
    let badgeDesc = "Você demonstrou alto discernimento ético, empatia e conhecimento das práticas que promovem a inclusão na Engenharia de Software.";

    if (this.score < 25) {
      badgeTitle = "Embaixador(a) em Formação de Equidade";
      badgeDesc = "Você começou a reconhecer os vieses. Vale a pena revisar as diretrizes de ética ACM/IEEE e o Programa Meninas Digitais da SBC para aprofundar seu impacto!";
    }

    container.innerHTML = `
      <div class="glass-card sim-finished-card">
        <div class="sim-trophy" aria-hidden="true">🎖️</div>
        <h2>Simulação Concluída com Sucesso!</h2>
        <p>Você vivenciou 5 dilemas reais da rotina de times de desenvolvimento de software.</p>
        
        <div class="sim-result-badge">${badgeTitle}</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-ods5-light); margin-bottom: 0.8rem;">
          ${this.score} / ${maxScore} Pontos Obtidos
        </div>
        <p style="max-width: 600px; margin: 0 auto 2rem; color: var(--text-secondary);">
          ${badgeDesc}
        </p>

        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="App.switchTab('mural')">
            ✍️ Registrar Meu Compromisso no Mural HeForShe
          </button>
          <button class="btn btn-secondary" onclick="SimulatorModule.init()">
            🔄 Repetir a Simulação
          </button>
        </div>
      </div>
    `;
  }
};
