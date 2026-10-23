/**
 * MenHelpHer - Lógica do Painel de Indicadores
 * Autor: Julio Costa 
 */

const DashboardModule = {
  init() {
    this.renderKPIs();
    this.renderFunnel();
    this.renderGoals();
  },

  renderKPIs() {
    const container = document.getElementById('kpiGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.indicadores.map(item => `
      <div class="kpi-card ${item.destaque}" tabindex="0" aria-label="${item.titulo}: ${item.valor}">
        <div class="kpi-top">
          <span class="kpi-title">${item.titulo}</span>
          <span class="kpi-icon" aria-hidden="true">📊</span>
        </div>
        <div class="kpi-value">${item.valor}</div>
        <p class="kpi-desc">${item.descricao}</p>
        <div class="kpi-footer">
          <span class="kpi-source">${item.fonte}</span>
          <span class="kpi-trend">${item.variacao}</span>
        </div>
      </div>
    `).join('');
  },

  renderFunnel() {
    const container = document.getElementById('funnelContainer');
    if (!container) return;

    container.innerHTML = EQUI_DATA.funilCarreira.map(item => `
      <div class="funnel-item" tabindex="0" aria-label="${item.etapa}: ${item.percentualMulheres}% mulheres, ${item.percentualHomens}% homens">
        <div class="funnel-labels">
          <span><strong>${item.etapa}</strong></span>
          <span>
            <strong style="color: var(--color-ods5-light);">${item.percentualMulheres}% Mulheres</strong> 
            <span style="color: var(--text-muted);">| ${item.percentualHomens}% Homens</span>
          </span>
        </div>
        <div class="funnel-track" role="progressbar" aria-valuenow="${item.percentualMulheres}" aria-valuemin="0" aria-valuemax="100">
          <div class="funnel-bar-women" style="width: ${item.percentualMulheres}%;">
            ${item.percentualMulheres}%
          </div>
          <div class="funnel-bar-men"></div>
        </div>
      </div>
    `).join('');
  },

  renderGoals() {
    const container = document.getElementById('goalsGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.metasOds5.map(meta => `
      <div class="goal-card" tabindex="0">
        <span class="goal-tag">${meta.codigo}</span>
        <h3>${meta.nome}</h3>
        <p>${meta.descricao}</p>
        <div class="goal-tech-box">
          <strong>Aplicação Prática em Engenharia de Software:</strong>
          <span>${meta.aplicacaoTech}</span>
        </div>
      </div>
    `).join('');
  }
};
