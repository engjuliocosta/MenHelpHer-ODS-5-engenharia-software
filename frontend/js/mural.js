/**
 * MenHelpHer ODS 5 - Lógica do Mural de Compromissos (HeForShe) & Avaliação de Impacto
 * Autor: Julio Costa
 *
 * Fluxo de dados: API REST (SQLite) -> fallback automático para localStorage quando
 * o servidor está indisponível (ex.: index.html aberto direto pelo navegador).
 */

const CHAVE_LOCAL_COMPROMISSOS = 'equitech_compromissos_v2';
const CHAVE_LOCAL_APOIADOS = 'equitech_apoiados';
const CHAVE_LOCAL_AVALIACOES = 'equitech_avaliacoes_pendentes';

const MuralModule = {
  compromissos: [],
  filtroAtual: 'todos',
  offline: false,
  apoiados: new Set(),

  async init() {
    this.apoiados = this.lerLocal(CHAVE_LOCAL_APOIADOS, []).reduce((s, id) => s.add(String(id)), new Set());
    await this.carregarCompromissos();
    this.renderCompromissos();
    this.renderPioneiras();
    this.renderChecklist();
    this.setupFormListeners();
    this.setupFeedListeners();
    this.carregarMetricas();
  },

  // ------------------------------------------------------------- persistência --
  lerLocal(chave, padrao) {
    try {
      const valor = JSON.parse(localStorage.getItem(chave));
      return valor ?? padrao;
    } catch (e) {
      return padrao;
    }
  },

  gravarLocal(chave, valor) {
    try {
      localStorage.setItem(chave, JSON.stringify(valor));
    } catch (e) {
      console.warn('Não foi possível gravar no armazenamento local.', e);
    }
  },

  async carregarCompromissos() {
    try {
      this.compromissos = await Api.listarCompromissos();
      this.definirModoOffline(false);
    } catch (e) {
      if (!(e instanceof ApiError)) throw e;
      this.compromissos = this.lerLocal(CHAVE_LOCAL_COMPROMISSOS, null) || this.getDefaultCompromissos();
      this.definirModoOffline(true);
    }
  },

  definirModoOffline(offline) {
    this.offline = offline;
    const aviso = document.getElementById('muralStatus');
    if (!aviso) return;
    aviso.hidden = !offline;
    aviso.textContent = offline
      ? 'ℹ️ Modo offline: o servidor não respondeu. Seus compromissos e apoios ficam salvos apenas neste navegador.'
      : '';
  },

  getDefaultCompromissos() {
    return [
      { id: 'demo-5', nome: 'Rodrigo Albuquerque', papel: 'Recrutador(a) Técnico (Tech Recruiter)', tipo: 'Equidade Salarial', tipo_label: 'Contratação Justa', mensagem: 'Adotamos triagem de currículos anônima nas etapas iniciais e garantimos equidade salarial na proposta inicial independentemente de histórico ou negociação prévia.', data: '11/10/2026', apoios: 39 },
      { id: 'demo-4', nome: 'Camila Duarte Mendes', papel: 'Engenheiro(a) de Software Pleno/Sênior', tipo: 'Liderança Técnica', tipo_label: 'Fomento à Liderança', mensagem: 'Criei círculos de mentoria para apoiar desenvolvedoras juniores e plenas rumo a posições sênior e de liderança tecnológica na empresa.', data: '12/10/2026', apoios: 51 },
      { id: 'demo-3', nome: 'Lucas Martins Silva', papel: 'Tech Lead / Arquiteto(a) de Software', tipo: 'Combate ao Manterrupting', tipo_label: 'Voz Ativa nas Reuniões', mensagem: 'Garantirei que nenhuma mulher seja interrompida durante os refinamentos e dailies da sprint. Se houver corte de fala, intervirei imediatamente para devolver a palavra à engenheira.', data: '14/10/2026', apoios: 35 },
      { id: 'demo-2', nome: 'Profa. Dra. Elena Vasconcelos', papel: 'Docente Universitário(a)', tipo: 'Mentoria Ativa', tipo_label: 'Mentoria & Apoio', mensagem: 'Incentivo ativamente a participação de alunas em grupos de iniciação científica e maratonas de programação, garantindo representatividade nas bancas avaliadoras.', data: '15/10/2026', apoios: 42 },
      { id: 'demo-1', nome: 'Julio Costa', papel: 'Estudante de Engenharia de Software', tipo: 'Code Review Inclusivo', tipo_label: 'Revisão Respeitosa', mensagem: 'Comprometo-me a revisar Pull Requests com critérios puramente técnicos e acolhedores, sem pré-julgamentos, e incentivar a autoria de colegas mulheres nas decisões de arquitetura de software.', data: '16/10/2026', apoios: 29 },
    ];
  },

  // ------------------------------------------------------------------ feed --
  setFilter(filtro) {
    this.filtroAtual = filtro;
    document.querySelectorAll('.filter-pill').forEach((btn) => {
      const ativo = btn.dataset.filter === filtro;
      btn.classList.toggle('active', ativo);
      btn.setAttribute('aria-pressed', String(ativo));
    });
    this.renderCompromissos();
  },

  atualizarContadores() {
    const countEl = document.getElementById('totalCommitmentsCount');
    const alliesEl = document.getElementById('totalAlliesCount');
    if (countEl) countEl.textContent = this.compromissos.length;
    if (alliesEl) alliesEl.textContent = Utils.somarApoios(this.compromissos);
  },

  renderCompromissos() {
    const feed = document.getElementById('commitmentsFeed');
    if (!feed) return;

    const lista = Utils.filtrarCompromissos(this.compromissos, this.filtroAtual);
    this.atualizarContadores();

    if (lista.length === 0) {
      feed.innerHTML = `<div class="feed-empty">Nenhum compromisso encontrado nesta categoria. Seja o primeiro a assinar!</div>`;
      return;
    }

    const esc = Utils.escapeHtml;
    feed.innerHTML = lista
      .map((comp) => {
        const inicial = comp.nome ? esc(comp.nome.trim().charAt(0).toUpperCase()) : 'U';
        const jaApoiou = this.apoiados.has(String(comp.id));
        return `
        <article class="commitment-card" id="card-${esc(comp.id)}" tabindex="0">
          <div class="commitment-meta">
            <div class="committer-info">
              <div class="committer-avatar" aria-hidden="true">${inicial}</div>
              <div class="committer-details">
                <span class="committer-name">${esc(comp.nome)}</span>
                <span class="committer-role">${esc(comp.papel)}</span>
              </div>
            </div>
            <span class="commitment-badge">${esc(comp.tipo_label || comp.tipo)}</span>
          </div>
          <blockquote class="commitment-text">"${esc(comp.mensagem)}"</blockquote>
          <div class="commitment-bottom">
            <span>📅 ${esc(comp.data)}</span>
            <button type="button" class="btn-like${jaApoiou ? ' liked' : ''}" data-action="apoiar" data-id="${esc(comp.id)}"
              aria-pressed="${jaApoiou}" ${jaApoiou ? 'disabled' : ''}
              aria-label="${jaApoiou ? 'Você já apoiou este compromisso' : 'Apoiar este compromisso'}">
              ❤️ <span id="likes-${esc(comp.id)}">${Number(comp.apoios) || 0}</span> Apoios
            </button>
          </div>
        </article>`;
      })
      .join('');
  },

  setupFeedListeners() {
    const feed = document.getElementById('commitmentsFeed');
    if (!feed) return;
    feed.addEventListener('click', (evento) => {
      const botao = evento.target.closest('[data-action="apoiar"]');
      if (botao) this.darApoio(botao.dataset.id);
    });
    document.querySelectorAll('.filter-pill').forEach((btn) => {
      btn.addEventListener('click', () => this.setFilter(btn.dataset.filter));
    });
  },

  async darApoio(id) {
    const chave = String(id);
    const comp = this.compromissos.find((c) => String(c.id) === chave);
    if (!comp || this.apoiados.has(chave)) return;

    try {
      if (this.offline || chave.startsWith('local-') || chave.startsWith('demo-')) {
        throw new ApiError('offline', 0);
      }
      const atualizado = await Api.apoiarCompromisso(comp.id);
      comp.apoios = atualizado.apoios;
    } catch (e) {
      if (!(e instanceof ApiError)) throw e;
      if (!e.semConexao) {
        this.mostrarMensagem('muralFeedback', `⚠️ ${e.message}`, 'erro');
        return;
      }
      comp.apoios = (Number(comp.apoios) || 0) + 1; // apoio local (modo offline)
      this.gravarLocal(CHAVE_LOCAL_COMPROMISSOS, this.compromissos);
    }

    this.apoiados.add(chave);
    this.gravarLocal(CHAVE_LOCAL_APOIADOS, [...this.apoiados]);
    this.renderCompromissos();
    const botao = document.querySelector(`[data-action="apoiar"][data-id="${CSS.escape(chave)}"]`);
    if (botao) botao.focus();
  },

  // ----------------------------------------------------------- formulários --
  mostrarMensagem(id, texto, tipo = 'sucesso', duracao = 5000) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = texto;
    el.dataset.tipo = tipo;
    el.style.display = 'block';
    clearTimeout(el._timer);
    el._timer = setTimeout(() => { el.style.display = 'none'; }, duracao);
  },

  mostrarErrosCampos(mapaCampos, erros) {
    Object.entries(mapaCampos).forEach(([campo, idInput]) => {
      const input = document.getElementById(idInput);
      const erroEl = document.getElementById(`err-${idInput}`);
      const msg = erros[campo] || '';
      if (erroEl) erroEl.textContent = msg;
      if (input) {
        input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      }
    });
    const primeiro = Object.entries(mapaCampos).find(([campo]) => erros[campo]);
    if (primeiro) document.getElementById(primeiro[1])?.focus();
  },

  setupFormListeners() {
    this.setupFormCompromisso();
    this.setupFormAvaliacao();
  },

  setupFormCompromisso() {
    const form = document.getElementById('commitmentForm');
    if (!form) return;
    const campos = { nome: 'committerName', mensagem: 'commitmentMsg', papel: 'committerRole', tipo: 'commitmentType' };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const dados = {
        nome: document.getElementById('committerName').value.trim(),
        papel: document.getElementById('committerRole').value,
        tipo: document.getElementById('commitmentType').value,
        mensagem: document.getElementById('commitmentMsg').value.trim(),
      };

      const erros = Utils.validarCompromisso(dados);
      this.mostrarErrosCampos(campos, erros);
      if (Object.keys(erros).length) return;

      const botao = form.querySelector('button[type="submit"]');
      botao.disabled = true;
      try {
        const gravado = await Api.criarCompromisso(dados);
        this.compromissos.unshift(gravado);
        this.definirModoOffline(false);
      } catch (err) {
        if (!(err instanceof ApiError)) throw err;
        if (!err.semConexao) {
          this.mostrarErrosCampos(campos, err.campos);
          this.mostrarMensagem('formErrorMsg', `⚠️ ${err.message}`, 'erro');
          return;
        }
        const tipoSelect = document.getElementById('commitmentType');
        this.compromissos.unshift({
          id: `local-${Date.now()}`,
          ...dados,
          tipo_label: tipoSelect.selectedOptions[0]?.dataset.label || dados.tipo,
          data: new Date().toLocaleDateString('pt-BR'),
          apoios: 1,
        });
        this.gravarLocal(CHAVE_LOCAL_COMPROMISSOS, this.compromissos);
        this.definirModoOffline(true);
      } finally {
        botao.disabled = false;
      }

      form.reset();
      this.mostrarErrosCampos(campos, {});
      this.renderCompromissos();
      this.mostrarMensagem('formSuccessMsg', '✅ Seu compromisso foi publicado com sucesso no mural!', 'sucesso', 4000);
    });
  },

  setupFormAvaliacao() {
    const form = document.getElementById('evalForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        perfil: document.getElementById('evalPerfil').value,
        clareza: parseInt(document.getElementById('evalClareza').value, 10),
        aprendizado_vieses: parseInt(document.getElementById('evalVieses').value, 10),
        relevancia_ods5: parseInt(document.getElementById('evalOds').value, 10),
        comentario: document.getElementById('evalComentario').value.trim(),
      };

      if (payload.comentario.length > Utils.LIMITES.comentarioMax) {
        this.mostrarMensagem('evalErrorMsg', `⚠️ O comentário deve ter no máximo ${Utils.LIMITES.comentarioMax} caracteres.`, 'erro');
        return;
      }

      const botao = form.querySelector('button[type="submit"]');
      botao.disabled = true;
      let mensagem = '🎉 Obrigado! Sua avaliação foi registrada e computada nas métricas do projeto.';
      try {
        await Api.enviarAvaliacao(payload);
      } catch (err) {
        if (!(err instanceof ApiError)) throw err;
        if (!err.semConexao) {
          this.mostrarMensagem('evalErrorMsg', `⚠️ ${err.message}`, 'erro');
          return;
        }
        const pendentes = this.lerLocal(CHAVE_LOCAL_AVALIACOES, []);
        pendentes.push({ ...payload, data: new Date().toISOString() });
        this.gravarLocal(CHAVE_LOCAL_AVALIACOES, pendentes);
        mensagem = 'ℹ️ Servidor indisponível: sua avaliação foi guardada neste navegador (não entrou nas métricas do projeto).';
      } finally {
        botao.disabled = false;
      }

      form.reset();
      this.mostrarMensagem('evalSuccessMsg', mensagem, 'sucesso', 6000);
      this.carregarMetricas();
    });
  },

  // -------------------------------------------------------------- métricas --
  async carregarMetricas() {
    const painel = document.getElementById('metricasCampanha');
    if (!painel) return;
    try {
      const m = await Api.obterMetricas();
      const fmt = (v) => (v === null || v === undefined ? '–' : String(v).replace('.', ','));
      document.getElementById('metTotalAvaliacoes').textContent = m.total_avaliacoes;
      document.getElementById('metClareza').textContent = fmt(m.media_clareza);
      document.getElementById('metVieses').textContent = fmt(m.media_aprendizado_vieses);
      document.getElementById('metOds5').textContent = fmt(m.media_relevancia_ods5);
      painel.hidden = false;
    } catch (e) {
      if (!(e instanceof ApiError)) throw e;
      painel.hidden = true;
    }
  },

  // -------------------------------------------------- conteúdo estático (data.js) --
  renderPioneiras() {
    const container = document.getElementById('pioneirasGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.pioneirasTech.map((p) => `
      <div class="glass-card pioneira-card" tabindex="0">
        <div class="pioneira-periodo">${p.periodo}</div>
        <h3>${p.nome}</h3>
        <div class="pioneira-titulo">${p.titulo}</div>
        <p>${p.contribuicao}</p>
        <div class="pioneira-legado">Legado: ${p.legado}</div>
      </div>
    `).join('');
  },

  renderChecklist() {
    const container = document.getElementById('checklistGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.checklistBoasPraticas.map((item, idx) => `
      <div class="glass-card checklist-card" tabindex="0">
        <div class="checklist-head">
          <span class="checklist-num">${idx + 1}</span>
          <strong>${item.titulo}</strong>
        </div>
        <p>${item.descricao}</p>
      </div>
    `).join('');
  },
};
