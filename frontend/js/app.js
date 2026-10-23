/**
 * EquiTech ODS 5 / MenHelpHer - Controlador Principal da Aplicação
 * Autor: Julio Costa
 * Curso: Engenharia de Software | Projeto Integrado Transdisciplinar
 */

const App = {
  currentTab: 'dashboard',
  theme: 'dark',
  highContrast: false,
  fontSizeFactor: 1.0,
  speechSynth: window.speechSynthesis,
  isSpeaking: false,

  init() {
    this.setupTheme();
    this.setupTabs();
    this.setupA11y();
    this.restoreA11yPrefs();
    this.setupMobileMenu();
    this.switchTab(this.currentTab); // sincroniza aria-selected / tabindex inicial

    // Inicializar módulos
    DashboardModule.init();
    SimulatorModule.init();
    MuralModule.init();
  },

  setupTheme() {
    const savedTheme = localStorage.getItem('equitech_theme') || 'dark';
    this.setTheme(savedTheme);
  },

  setTheme(themeName) {
    this.theme = themeName;
    document.documentElement.setAttribute('data-theme', themeName);
    localStorage.setItem('equitech_theme', themeName);

    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
      themeBtn.innerHTML = themeName === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Escuro';
    }
  },

  toggleTheme() {
    this.setTheme(this.theme === 'dark' ? 'light' : 'dark');
  },

  setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn, .nav-link[data-tab]');
    tabButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = btn.dataset.tab;
        if (tab) {
          e.preventDefault();
          this.switchTab(tab);
        }
      });
    });

    // Navegação por teclado (padrão WAI-ARIA Tabs): setas, Home e End.
    const tabs = Array.from(document.querySelectorAll('.tab-btn'));
    tabs.forEach((btn, idx) => {
      btn.addEventListener('keydown', (e) => {
        let destino = null;
        if (e.key === 'ArrowRight') destino = (idx + 1) % tabs.length;
        else if (e.key === 'ArrowLeft') destino = (idx - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') destino = 0;
        else if (e.key === 'End') destino = tabs.length - 1;
        if (destino === null) return;
        e.preventDefault();
        tabs[destino].focus();
        this.switchTab(tabs[destino].dataset.tab);
      });
    });
  },

  switchTab(tabId) {
    this.currentTab = tabId;

    // Atualizar botões de abas
    document.querySelectorAll('.tab-btn').forEach(btn => {
      const ativo = btn.dataset.tab === tabId;
      btn.classList.toggle('active', ativo);
      btn.setAttribute('aria-selected', String(ativo));
      btn.tabIndex = ativo ? 0 : -1; // roving tabindex
    });

    // Atualizar links da navbar
    document.querySelectorAll('.nav-link[data-tab]').forEach(link => {
      const ativo = link.dataset.tab === tabId;
      link.classList.toggle('active', ativo);
      if (ativo) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });

    // Atualizar painéis
    document.querySelectorAll('.tab-pane').forEach(pane => {
      pane.classList.toggle('active', pane.id === `tab-${tabId}`);
    });

    // Fechar menu mobile se aberto
    const navLinks = document.getElementById('navLinks');
    if (navLinks && navLinks.classList.contains('open')) {
      navLinks.classList.remove('open');
    }

    // Scroll suave para o conteúdo principal
    const contentArea = document.getElementById('mainContentArea');
    if (contentArea && window.scrollY > 300) {
      window.scrollTo({ top: contentArea.offsetTop - 80, behavior: 'smooth' });
    }
  },

  setHighContrast(ativo) {
    this.highContrast = ativo;
    document.documentElement.setAttribute('data-high-contrast', ativo ? 'true' : 'false');
    const contrastBtn = document.getElementById('contrastToggleBtn');
    if (contrastBtn) {
      contrastBtn.classList.toggle('active', ativo);
      contrastBtn.setAttribute('aria-pressed', String(ativo));
    }
    localStorage.setItem('equitech_contrast', ativo ? '1' : '0');
  },

  setFontScale(fator) {
    this.fontSizeFactor = Math.min(1.35, Math.max(0.85, Math.round(fator * 100) / 100));
    document.documentElement.style.setProperty('--font-scale-factor', this.fontSizeFactor);
    localStorage.setItem('equitech_font_scale', String(this.fontSizeFactor));
  },

  /** Restaura preferências de acessibilidade salvas (contraste e tamanho da fonte). */
  restoreA11yPrefs() {
    this.setHighContrast(localStorage.getItem('equitech_contrast') === '1');
    const fator = parseFloat(localStorage.getItem('equitech_font_scale'));
    if (!Number.isNaN(fator)) this.setFontScale(fator);
  },

  setupA11y() {
    // Alto Contraste
    const contrastBtn = document.getElementById('contrastToggleBtn');
    if (contrastBtn) {
      contrastBtn.addEventListener('click', () => this.setHighContrast(!this.highContrast));
    }

    // Aumento de Fonte
    const fontPlusBtn = document.getElementById('fontPlusBtn');
    const fontMinusBtn = document.getElementById('fontMinusBtn');
    const fontResetBtn = document.getElementById('fontResetBtn');

    if (fontPlusBtn) fontPlusBtn.addEventListener('click', () => this.setFontScale(this.fontSizeFactor + 0.08));
    if (fontMinusBtn) fontMinusBtn.addEventListener('click', () => this.setFontScale(this.fontSizeFactor - 0.08));
    if (fontResetBtn) fontResetBtn.addEventListener('click', () => this.setFontScale(1.0));

    // Leitor de Tela Web Speech API
    const ttsBtn = document.getElementById('ttsToggleBtn');
    if (ttsBtn && 'speechSynthesis' in window) {
      ttsBtn.addEventListener('click', () => {
        if (this.isSpeaking) {
          this.speechSynth.cancel();
          this.isSpeaking = false;
          ttsBtn.classList.remove('active');
          ttsBtn.innerHTML = '🔊 Ler Tela';
        } else {
          const activePane = document.querySelector('.tab-pane.active');
          if (!activePane) return;
          const textToRead = activePane.innerText;
          const utterance = new SpeechSynthesisUtterance(textToRead.slice(0, 4000));
          utterance.lang = 'pt-BR';
          utterance.rate = 1.05;

          utterance.onend = () => {
            this.isSpeaking = false;
            ttsBtn.classList.remove('active');
            ttsBtn.innerHTML = '🔊 Ler Tela';
          };

          this.speechSynth.speak(utterance);
          this.isSpeaking = true;
          ttsBtn.classList.add('active');
          ttsBtn.innerHTML = '⏹️ Parar Leitura';
        }
      });
    } else if (ttsBtn) {
      ttsBtn.style.display = 'none';
    }
  },

  setupMobileMenu() {
    const toggle = document.getElementById('navToggleBtn');
    const navLinks = document.getElementById('navLinks');
    if (toggle && navLinks) {
      toggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
