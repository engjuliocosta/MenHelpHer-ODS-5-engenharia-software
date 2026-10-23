-- Dados de demonstração - MenHelpHer ODS 5
-- Registros ilustrativos herdados do PIT I. Carregados SOMENTE quando o banco é
-- criado do zero (tabelas de compromissos e avaliações vazias).

PRAGMA foreign_keys = ON;

-- Compromissos (do mais antigo ao mais recente)
INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios, criado_em) VALUES (
  'Rodrigo Albuquerque',
  (SELECT id FROM papel WHERE nome = 'Recrutador(a) Técnico (Tech Recruiter)'),
  (SELECT id FROM tipo_compromisso WHERE codigo = 'Equidade Salarial'),
  'Adotamos triagem de currículos anônima nas etapas iniciais e garantimos equidade salarial na proposta inicial independentemente de histórico ou negociação prévia.',
  39, '2026-10-11 12:00:00');
INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios, criado_em) VALUES (
  'Camila Duarte Mendes',
  (SELECT id FROM papel WHERE nome = 'Engenheiro(a) de Software Pleno/Sênior'),
  (SELECT id FROM tipo_compromisso WHERE codigo = 'Liderança Técnica'),
  'Criei círculos de mentoria para apoiar desenvolvedoras juniores e plenas rumo a posições sênior e de liderança tecnológica na empresa.',
  51, '2026-10-12 12:00:00');
INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios, criado_em) VALUES (
  'Lucas Martins Silva',
  (SELECT id FROM papel WHERE nome = 'Tech Lead / Arquiteto(a) de Software'),
  (SELECT id FROM tipo_compromisso WHERE codigo = 'Combate ao Manterrupting'),
  'Garantirei que nenhuma mulher seja interrompida durante os refinamentos e dailies da sprint. Se houver corte de fala, intervirei imediatamente para devolver a palavra à engenheira.',
  35, '2026-10-14 12:00:00');
INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios, criado_em) VALUES (
  'Profa. Dra. Elena Vasconcelos',
  (SELECT id FROM papel WHERE nome = 'Docente Universitário(a)'),
  (SELECT id FROM tipo_compromisso WHERE codigo = 'Mentoria Ativa'),
  'Incentivo ativamente a participação de alunas em grupos de iniciação científica e maratonas de programação, garantindo representatividade nas bancas avaliadoras.',
  42, '2026-10-15 12:00:00');
INSERT INTO compromisso (nome, papel_id, tipo_id, mensagem, apoios, criado_em) VALUES (
  'Julio Costa',
  (SELECT id FROM papel WHERE nome = 'Estudante de Engenharia de Software'),
  (SELECT id FROM tipo_compromisso WHERE codigo = 'Code Review Inclusivo'),
  'Comprometo-me a revisar Pull Requests com critérios puramente técnicos e acolhedores, sem pré-julgamentos, e incentivar a autoria de colegas mulheres nas decisões de arquitetura de software.',
  29, '2026-10-16 12:00:00');

-- Avaliações de impacto (do mais antigo ao mais recente)
INSERT INTO avaliacao (perfil_id, clareza, aprendizado_vieses, relevancia_ods5, comentario, criado_em) VALUES (
  (SELECT id FROM perfil_avaliador WHERE nome = 'Docente'),
  5, 5, 5,
  'Vou utilizar o quiz como dinâmica nas aulas de Ética e Legislação em Computação.', '2026-10-15 12:00:00');
INSERT INTO avaliacao (perfil_id, clareza, aprendizado_vieses, relevancia_ods5, comentario, criado_em) VALUES (
  (SELECT id FROM perfil_avaliador WHERE nome = 'Profissional de TI'),
  5, 4, 5,
  'Excelente iniciativa. Os dados do IPEA e SBC sobre o gap salarial e a baixa representatividade precisam ser amplamente divulgados nos squads.', '2026-10-15 12:00:00');
INSERT INTO avaliacao (perfil_id, clareza, aprendizado_vieses, relevancia_ods5, comentario, criado_em) VALUES (
  (SELECT id FROM perfil_avaliador WHERE nome = 'Estudante'),
  5, 5, 5,
  'O simulador de situações reais me fez perceber situações em que colegas foram interrompidas em reuniões acadêmicas sem que eu notasse.', '2026-10-16 12:00:00');
