/**
 * MenHelpHer ODS 5 - Cliente da API REST (camada de acesso do front-end ao back-end).
 * Autor: Julio Costa
 */

class ApiError extends Error {
  constructor(mensagem, status = 0, campos = {}) {
    super(mensagem);
    this.name = 'ApiError';
    this.status = status;
    this.campos = campos;
  }

  /** true quando não houve resposta do servidor (offline, timeout ou página aberta via file://). */
  get semConexao() {
    return this.status === 0;
  }
}

const Api = {
  // Aberto via file:// (duplo clique), tenta o servidor local padrão.
  base: window.location.protocol === 'file:' ? 'http://localhost:8000' : '',
  timeoutMs: 6000,

  async request(caminho, { method = 'GET', corpo } = {}) {
    const controle = new AbortController();
    const timer = setTimeout(() => controle.abort(), this.timeoutMs);
    let resposta;
    try {
      resposta = await fetch(this.base + caminho, {
        method,
        headers: corpo !== undefined ? { 'Content-Type': 'application/json' } : undefined,
        body: corpo !== undefined ? JSON.stringify(corpo) : undefined,
        signal: controle.signal,
      });
    } catch (e) {
      throw new ApiError('Servidor indisponível.', 0);
    } finally {
      clearTimeout(timer);
    }

    let dados = null;
    try {
      dados = await resposta.json();
    } catch (e) {
      /* resposta sem JSON (ex.: servidor estático sem API) */
    }
    if (!resposta.ok) {
      // 404/405 de servidor estático sem API equivale a "sem back-end".
      if (!dados || !dados.erro) throw new ApiError('Servidor indisponível.', 0);
      throw new ApiError(dados.erro, resposta.status, dados.campos || {});
    }
    return dados;
  },

  listarCompromissos: () => Api.request('/api/compromissos'),
  criarCompromisso: (dados) => Api.request('/api/compromissos', { method: 'POST', corpo: dados }),
  apoiarCompromisso: (id) => Api.request(`/api/compromissos/${encodeURIComponent(id)}/apoios`, { method: 'POST' }),
  enviarAvaliacao: (dados) => Api.request('/api/avaliacoes', { method: 'POST', corpo: dados }),
  obterMetricas: () => Api.request('/api/metricas'),
};
