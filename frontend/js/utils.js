/**
 * MenHelpHer ODS 5 - Funções utilitárias puras (sem acesso ao DOM).
 * Isoladas para permitir testes automatizados (frontend/tests/index.html).
 * Autor: Julio Costa
 */

const Utils = (() => {
  const MAPA_ESCAPE = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

  /** Escapa texto para inserção segura em HTML (previne XSS em conteúdo de usuário). */
  function escapeHtml(valor) {
    return String(valor ?? '').replace(/[&<>"']/g, (c) => MAPA_ESCAPE[c]);
  }

  /** Minúsculas e sem acentos, para comparações tolerantes. */
  function normalizar(texto) {
    return String(texto ?? '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  }

  /** Filtra compromissos pelo papel. `todos` não filtra. */
  function filtrarCompromissos(lista, filtro) {
    if (!filtro || filtro === 'todos') return lista.slice();
    const alvo = normalizar(filtro);
    return lista.filter((c) => normalizar(c.papel).includes(alvo));
  }

  function somarApoios(lista) {
    return lista.reduce((total, c) => total + (Number(c.apoios) || 0), 0);
  }

  const LIMITES = { nomeMin: 2, nomeMax: 80, mensagemMin: 10, mensagemMax: 500, comentarioMax: 500 };

  /** Valida o formulário de compromisso. Retorna objeto {campo: mensagem} (vazio = válido). */
  function validarCompromisso({ nome, mensagem }) {
    const erros = {};
    const n = String(nome ?? '').trim();
    const m = String(mensagem ?? '').trim();
    if (n.length < LIMITES.nomeMin || n.length > LIMITES.nomeMax) {
      erros.nome = `Informe um nome com ${LIMITES.nomeMin} a ${LIMITES.nomeMax} caracteres.`;
    }
    if (m.length < LIMITES.mensagemMin || m.length > LIMITES.mensagemMax) {
      erros.mensagem = `A declaração deve ter entre ${LIMITES.mensagemMin} e ${LIMITES.mensagemMax} caracteres.`;
    }
    return erros;
  }

  /** Classifica o resultado final do simulador (limiar de 50% da pontuação máxima). */
  function classificarResultado(pontos, maximo) {
    const aliado = maximo > 0 && pontos / maximo >= 0.5;
    return aliado
      ? {
          nivel: 'aliado',
          titulo: 'Engenheiro(a) Aliado(a) da Equidade ODS 5',
          descricao:
            'Você demonstrou alto discernimento ético, empatia e conhecimento das práticas que promovem a inclusão na Engenharia de Software.',
        }
      : {
          nivel: 'formacao',
          titulo: 'Embaixador(a) em Formação de Equidade',
          descricao:
            'Você começou a reconhecer os vieses. Vale a pena revisar as diretrizes de ética ACM/IEEE e o Programa Meninas Digitais da SBC para aprofundar seu impacto!',
        };
  }

  /** Classifica a pontuação de uma única escolha: correto | parcial | erro. */
  function classificarEscolha(pontos) {
    if (pontos >= 8) return 'correto';
    if (pontos > 0) return 'parcial';
    return 'erro';
  }

  return { escapeHtml, normalizar, filtrarCompromissos, somarApoios, validarCompromisso, classificarResultado, classificarEscolha, LIMITES };
})();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = Utils;
}
