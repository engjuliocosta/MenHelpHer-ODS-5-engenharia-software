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
    this.setupMobileMenu();

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
  },

  switchTab(tabId) {
    this.currentTab = tabId;

    // Atualizar botões de abas
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
      btn.setAttribute('aria-selected', btn.dataset.tab === tabId);
    });

    // Atualizar links da navbar
    document.querySelectorAll('.nav-link[data-tab]').forEach(link => {
      link.classList.toggle('active', link.dataset.tab === tabId);
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

  setupA11y() {
    // Alto Contraste
    const contrastBtn = document.getElementById('contrastToggleBtn');
    if (contrastBtn) {
      contrastBtn.addEventListener('click', () => {
        this.highContrast = !this.highContrast;
        document.documentElement.setAttribute('data-high-contrast', this.highContrast ? 'true' : 'false');
        contrastBtn.classList.toggle('active', this.highContrast);
      });
    }

    // Aumento de Fonte
    const fontPlusBtn = document.getElementById('fontPlusBtn');
    const fontMinusBtn = document.getElementById('fontMinusBtn');
    const fontResetBtn = document.getElementById('fontResetBtn');

    if (fontPlusBtn) {
      fontPlusBtn.addEventListener('click', () => {
        if (this.fontSizeFactor < 1.35) {
          this.fontSizeFactor += 0.08;
          document.documentElement.style.setProperty('--font-scale-factor', this.fontSizeFactor);
        }
      });
    }

    if (fontMinusBtn) {
      fontMinusBtn.addEventListener('click', () => {
        if (this.fontSizeFactor > 0.85) {
          this.fontSizeFactor -= 0.08;
          document.documentElement.style.setProperty('--font-scale-factor', this.fontSizeFactor);
        }
      });
    }

    if (fontResetBtn) {
      fontResetBtn.addEventListener('click', () => {
        this.fontSizeFactor = 1.0;
        document.documentElement.style.setProperty('--font-scale-factor', 1.0);
      });
    }

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
          const utterance = new SpeechSynthesisUtterance(textToRead.slice(0, 1000));
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
