-- Dados de domínio (catálogos) - MenHelpHer ODS 5
-- Idempotente: executado a cada inicialização, sem duplicar registros.
-- Os valores devem coincidir com as <option> dos formulários em frontend/index.html
-- (garantido pelo teste tests/test_frontend_estrutura.py).

PRAGMA foreign_keys = ON;

-- Papéis na comunidade de TI
INSERT OR IGNORE INTO papel (nome) VALUES ('Estudante de Engenharia de Software');
INSERT OR IGNORE INTO papel (nome) VALUES ('Estudante de Ciência da Computação / TI');
INSERT OR IGNORE INTO papel (nome) VALUES ('Docente Universitário(a)');
INSERT OR IGNORE INTO papel (nome) VALUES ('Engenheiro(a) de Software Pleno/Sênior');
INSERT OR IGNORE INTO papel (nome) VALUES ('Tech Lead / Arquiteto(a) de Software');
INSERT OR IGNORE INTO papel (nome) VALUES ('Recrutador(a) Técnico (Tech Recruiter)');

-- Tipos de compromisso (codigo = valor do formulário; rotulo = selo do cartão)
INSERT OR IGNORE INTO tipo_compromisso (codigo, rotulo) VALUES ('Code Review Inclusivo', 'Revisão Respeitosa');
INSERT OR IGNORE INTO tipo_compromisso (codigo, rotulo) VALUES ('Combate ao Manterrupting', 'Voz Ativa nas Reuniões');
INSERT OR IGNORE INTO tipo_compromisso (codigo, rotulo) VALUES ('Mentoria Ativa', 'Mentoria & Apoio');
INSERT OR IGNORE INTO tipo_compromisso (codigo, rotulo) VALUES ('Liderança Técnica', 'Fomento à Liderança');
INSERT OR IGNORE INTO tipo_compromisso (codigo, rotulo) VALUES ('Equidade Salarial', 'Contratação Justa');

-- Perfis de avaliadores
INSERT OR IGNORE INTO perfil_avaliador (nome) VALUES ('Estudante');
INSERT OR IGNORE INTO perfil_avaliador (nome) VALUES ('Docente');
INSERT OR IGNORE INTO perfil_avaliador (nome) VALUES ('Profissional de TI');
INSERT OR IGNORE INTO perfil_avaliador (nome) VALUES ('Outro');
