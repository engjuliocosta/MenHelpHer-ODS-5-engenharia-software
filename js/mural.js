/**
 * MenHelpHer ODS 5 - Lógica do Mural de Compromissos (HeForShe) & Avaliação de Impacto
 * Autor: Julio Costa 
 */

const MuralModule = {
  compromissos: [],
  filtroAtual: 'todos',

  async init() {
    await this.carregarCompromissos();
    this.renderCompromissos();
    this.renderPioneiras();
    this.renderChecklist();
    this.setupFormListeners();
  },

  async carregarCompromissos() {
    try {
      const response = await fetch('/api/compromissos');
      if (response.ok) {
        this.compromissos = await response.json();
        return;
      }
    } catch (e) {
      console.warn("API offline, utilizando armazenamento local.");
    }

    // Fallback: LocalStorage ou mock inicial
    const local = localStorage.getItem('equitech_compromissos');
    if (local) {
      try {
        this.compromissos = JSON.parse(local);
      } catch (err) {
        this.compromissos = this.getDefaultCompromissos();
      }
    } else {
      this.compromissos = this.getDefaultCompromissos();
    }
  },

  getDefaultCompromissos() {
    return [
      {
        id: "comp-1",
        nome: "Julio Costa",
        papel: "Estudante de Engenharia de Software",
        tipo: "Code Review Inclusivo",
        tipo_label: "Revisão de Código Respeitosa",
        mensagem: "Comprometo-me a revisar Pull Requests com critérios puramente técnicos e acolhedores, sem pré-julgamentos, e incentivar a autoria de colegas mulheres nas decisões de arquitetura de software.",
        data: "16/10/2026",
        likes: 28
      },
      {
        id: "comp-2",
        nome: "Profa. Dra. Elena Vasconcelos",
        papel: "Docente Universitária",
        tipo: "Mentoria Ativa",
        tipo_label: "Mentoria & Apoio Acadêmico",
        mensagem: "Incentivo ativamente a participação de alunas em grupos de iniciação científica e maratonas de programação, garantindo representatividade nas bancas avaliadoras.",
        data: "15/10/2026",
        likes: 42
      },
      {
        id: "comp-3",
        nome: "Lucas Martins Silva",
        papel: "Tech Lead / Arquiteto de Software",
        tipo: "Combate ao Manterrupting",
        tipo_label: "Voz Ativa nas Reuniões",
        mensagem: "Garantirei que nenhuma mulher seja interrompida durante os refinamentos e dailies da sprint. Se houver corte de fala, intervirei imediatamente para devolver a palavra à engenheira.",
        data: "14/10/2026",
        likes: 35
      },
      {
        id: "comp-4",
        nome: "Camila Duarte Mendes",
        papel: "Engenheira de Software Sênior",
        tipo: "Liderança Técnica",
        tipo_label: "Fomento à Liderança Feminina",
        mensagem: "Criei círculos de mentoria para apoiar desenvolvedoras juniores e plenas rumo a posições sênior e de liderança tecnológica na empresa.",
        data: "12/10/2026",
        likes: 51
      }
    ];
  },

  setFilter(filtro) {
    this.filtroAtual = filtro;
    document.querySelectorAll('.filter-pill').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.filter === filtro);
    });
    this.renderCompromissos();
  },

  renderCompromissos() {
    const feed = document.getElementById('commitmentsFeed');
    const countEl = document.getElementById('totalCommitmentsCount');
    const alliesEl = document.getElementById('totalAlliesCount');
    if (!feed) return;

    let lista = this.compromissos;
    if (this.filtroAtual !== 'todos') {
      lista = lista.filter(c => c.papel.toLowerCase().includes(this.filtroAtual.toLowerCase()));
    }

    if (countEl) countEl.innerText = this.compromissos.length;
    if (alliesEl) alliesEl.innerText = this.compromissos.reduce((acc, c) => acc + (c.likes || 1), 0);

    if (lista.length === 0) {
      feed.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
          Nenhum compromisso encontrado nesta categoria. Seja o primeiro a assinar!
        </div>
      `;
      return;
    }

    feed.innerHTML = lista.map(comp => {
      const inicial = comp.nome ? comp.nome.charAt(0).toUpperCase() : 'U';
      return `
        <article class="commitment-card" id="card-${comp.id}" tabindex="0">
          <div class="commitment-meta">
            <div class="committer-info">
              <div class="committer-avatar" aria-hidden="true">${inicial}</div>
              <div class="committer-details">
                <span class="committer-name">${comp.nome}</span>
                <span class="committer-role">${comp.papel}</span>
              </div>
            </div>
            <span class="commitment-badge">${comp.tipo_label || comp.tipo}</span>
          </div>
          <blockquote class="commitment-text">
            "${comp.mensagem}"
          </blockquote>
          <div class="commitment-bottom">
            <span>📅 ${comp.data}</span>
            <button class="btn-like" onclick="MuralModule.darApoio('${comp.id}')" aria-label="Apoiar este compromisso">
              ❤️ <span id="likes-${comp.id}">${comp.likes || 0}</span> Apoios
            </button>
          </div>
        </article>
      `;
    }).join('');
  },

  async darApoio(id) {
    const comp = this.compromissos.find(c => c.id === id);
    if (!comp) return;

    comp.likes = (comp.likes || 0) + 1;
    const likesEl = document.getElementById(`likes-${id}`);
    if (likesEl) likesEl.innerText = comp.likes;

    const alliesEl = document.getElementById('totalAlliesCount');
    if (alliesEl) alliesEl.innerText = this.compromissos.reduce((acc, c) => acc + (c.likes || 1), 0);

    // Tentar sincronizar via API
    try {
      await fetch('/api/compromissos/like', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      });
    } catch (e) {
      localStorage.setItem('equitech_compromissos', JSON.stringify(this.compromissos));
    }
  },

  setupFormListeners() {
    const form = document.getElementById('commitmentForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const nome = document.getElementById('committerName').value.trim();
      const papel = document.getElementById('committerRole').value;
      const tipo = document.getElementById('commitmentType').value;
      const mensagem = document.getElementById('commitmentMsg').value.trim();

      if (!nome || !mensagem) {
        alert("Por favor, preencha seu nome e sua mensagem de compromisso.");
        return;
      }

      const tipoLabelMap = {
        "Code Review Inclusivo": "Revisão Respeitosa",
        "Combate ao Manterrupting": "Voz Ativa nas Reuniões",
        "Mentoria Ativa": "Mentoria & Apoio",
        "Liderança Técnica": "Fomento à Liderança",
        "Equidade Salarial": "Contratação Justa"
      };

      const novoCompromisso = {
        id: `comp-${Date.now()}`,
        nome,
        papel,
        tipo,
        tipo_label: tipoLabelMap[tipo] || tipo,
        mensagem,
        data: new Date().toLocaleDateString('pt-BR'),
        likes: 1
      };

      // Tentar salvar via backend
      try {
        const response = await fetch('/api/compromissos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(novoCompromisso)
        });
        if (response.ok) {
          const gravado = await response.json();
          this.compromissos.unshift(gravado);
        } else {
          this.compromissos.unshift(novoCompromisso);
        }
      } catch (err) {
        this.compromissos.unshift(novoCompromisso);
        localStorage.setItem('equitech_compromissos', JSON.stringify(this.compromissos));
      }

      form.reset();
      this.renderCompromissos();

      const successToast = document.getElementById('formSuccessMsg');
      if (successToast) {
        successToast.style.display = 'block';
        setTimeout(() => { successToast.style.display = 'none'; }, 4000);
      }
    });

    // Form de Avaliação de Impacto
    const evalForm = document.getElementById('evalForm');
    if (evalForm) {
      evalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const perfil = document.getElementById('evalPerfil').value;
        const clareza = parseInt(document.getElementById('evalClareza').value);
        const aprendizado_vieses = parseInt(document.getElementById('evalVieses').value);
        const relevancia_ods5 = parseInt(document.getElementById('evalOds').value);
        const comentario = document.getElementById('evalComentario').value;

        const payload = { perfil, clareza, aprendizado_vieses, relevancia_ods5, comentario };

        try {
          await fetch('/api/avaliacoes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } catch (err) {
          console.log("Avaliação salva localmente");
        }

        const msg = document.getElementById('evalSuccessMsg');
        if (msg) {
          msg.style.display = 'block';
          evalForm.reset();
          setTimeout(() => { msg.style.display = 'none'; }, 5000);
        }
      });
    }
  },

  renderPioneiras() {
    const container = document.getElementById('pioneirasGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.pioneirasTech.map(p => `
      <div class="glass-card" tabindex="0">
        <div style="font-size: 0.8rem; font-weight: 700; color: var(--color-ods5-light); margin-bottom: 0.25rem;">
          ${p.periodo}
        </div>
        <h3 style="margin-bottom: 0.25rem;">${p.nome}</h3>
        <div style="font-size: 0.85rem; color: var(--color-primary-light); font-weight: 600; margin-bottom: 0.75rem;">
          ${p.titulo}
        </div>
        <p style="font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.75rem;">${p.contribuicao}</p>
        <div style="font-size: 0.8rem; font-style: italic; color: var(--text-muted); border-top: 1px solid var(--border-subtle); padding-top: 0.5rem;">
          Legado: ${p.legado}
        </div>
      </div>
    `).join('');
  },

  renderChecklist() {
    const container = document.getElementById('checklistGrid');
    if (!container) return;

    container.innerHTML = EQUI_DATA.checklistBoasPraticas.map((item, idx) => `
      <div class="glass-card" style="padding: 1.25rem;" tabindex="0">
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
          <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: var(--color-ods5); color: #fff; font-size: 0.75rem; font-weight: 700;">
            ${idx + 1}
          </span>
          <strong style="font-size: 0.95rem; color: var(--text-primary);">${item.titulo}</strong>
        </div>
        <p style="font-size: 0.86rem; color: var(--text-secondary); margin: 0;">${item.descricao}</p>
      </div>
    `).join('');
  }
};
