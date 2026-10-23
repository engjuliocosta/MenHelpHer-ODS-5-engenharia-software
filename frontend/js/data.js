/**
 * MenHelpHer ODS 5 - Base de Dados e Indicadores Oficiais
 * Aluno: Julio Costa 
 * Projeto Integrado Transdisciplinar - Engenharia de Software
 */

const EQUI_DATA = {
  projeto: {
    nome: "MenHelpHer ODS 5",
    subtitulo: "Plataforma de Sensibilização e Equidade de Gênero na Engenharia de Software",
    autor: "Julio Costa",
    curso: "Engenharia de Software",
    disciplina: "Projeto Integrado Transdisciplinar (PIT I e PIT II)",
    ano: "2026",
    movimentos: [
      "ODS 5 - Igualdade de Gênero (ONU Brasil / Agenda 2030)",
      "HeForShe / ElesPorElas (ONU Mulheres)",
      "Programa Meninas Digitais (Sociedade Brasileira de Computação - SBC)"
    ]
  },

  indicadores: [
    {
      id: "matriculas-computacao",
      valor: "15,2%",
      titulo: "Mulheres em Cursos de TI",
      descricao: "Proporção de alunas matriculadas em cursos superiores de Engenharia de Software, Ciência da Computação e Sistemas de Informação no Brasil.",
      fonte: "SBC / Censo da Educação Superior (Inep/MEC)",
      variacao: "-70% desde a década de 1980",
      destaque: "crítico",
      icone: "graduation-cap"
    },
    {
      id: "mercado-trabalho",
      valor: "17,8%",
      titulo: "Participação no Setor de TI",
      descricao: "Percentual de mulheres atuando em funções técnicas de tecnologia e desenvolvimento de sistemas no mercado brasileiro.",
      fonte: "IPEA / PNAD Contínua (Retrato das Desigualdades)",
      variacao: "Evolução lenta (+1,5% em 5 anos)",
      destaque: "alerta",
      icone: "briefcase"
    },
    {
      id: "lideranca-tecnica",
      valor: "13,6%",
      titulo: "Liderança Técnica (Meta 5.5)",
      descricao: "Mulheres em posições de liderança técnica (CTOs, VPs de Engenharia, Tech Leads e Arquitetas de Software).",
      fonte: "ONU Mulheres / ODS Brasil Relatório 2024",
      variacao: "Apenas 1 a cada 7 líderes em tech",
      destaque: "critico",
      icone: "award"
    },
    {
      id: "gap-salarial",
      valor: "21,4%",
      titulo: "Gap Salarial em Software",
      descricao: "Diferença média de remuneração entre homens e mulheres ocupando cargos equivalentes de engenharia de software na mesma senioridade.",
      fonte: "IPEA / Guia Salarial Tech & Robert Half",
      variacao: "Desigualdade atinge 26% em níveis sênior",
      destaque: "alerta",
      icone: "dollar-sign"
    }
  ],

  metasOds5: [
    {
      codigo: "Meta 5.1",
      nome: "Eliminar a Discriminação",
      descricao: "Acabar com todas as formas de discriminação contra todas as mulheres e meninas nas esferas pública e privada, erradicando barreiras culturais no ambiente tecnológico.",
      aplicacaoTech: "Políticas explícitas de tolerância zero ao assédio e microagressões em squads, canais de denúncia seguros e código de conduta ativo em repositórios e eventos."
    },
    {
      codigo: "Meta 5.5",
      nome: "Participação Plena e Liderança",
      descricao: "Garantir a participação plena e efetiva das mulheres e a igualdade de oportunidades para a liderança em todos os níveis de tomada de decisão.",
      aplicacaoTech: "Planos de carreira transparentes, programas de apadrinhamento e metas corporativas de paridade em conselhos técnicos e cargos de Tech Lead/CTO."
    },
    {
      codigo: "Meta 5.b",
      nome: "Empoderamento pelas TICs",
      descricao: "Aumentar o uso de tecnologias de base, em particular as tecnologias de informação e comunicação (TICs), para promover o empoderamento das mulheres.",
      aplicacaoTech: "Bolsas de estudo para formação técnica feminina, apoio a projetos comunitários (PyLadies, WoMakersCode, Meninas Digitais) e ferramentas de detecção de viés algorítmico."
    }
  ],

  funilCarreira: [
    { etapa: "Ingressantes na Graduação", percentualMulheres: 18, percentualHomens: 82 },
    { etapa: "Concluintes Universitárias", percentualMulheres: 15, percentualHomens: 85 },
    { etapa: "Engenheira Júnior", percentualMulheres: 22, percentualHomens: 78 },
    { etapa: "Engenheira Plena", percentualMulheres: 18, percentualHomens: 82 },
    { etapa: "Engenheira Sênior / Staff", percentualMulheres: 12, percentualHomens: 88 },
    { etapa: "Tech Lead / CTO / Diretoria", percentualMulheres: 9, percentualHomens: 91 }
  ],

  cenariosSimulador: [
    {
      id: 1,
      titulo: "Code Review com Exigências Desproporcionais",
      categoria: "Revisão de Código & Engenharia de Requisitos",
      situacao: "Mariana, Engenheira de Software Sênior, submeteu um Pull Request reestruturando o subsistema de autenticação OAuth2 com cobertura de 98% em testes unitários. Na revisão, um colega escreveu 24 comentários pedantes sobre estilo estético e perguntou 'Tem certeza de que você entende como funciona a criptografia disso? Talvez devesse passar pro Bruno'. No mesmo dia, um colega homem submeteu um PR de código crítico sem testes e foi aprovado com um simples 'LGTM 🚀'.",
      pergunta: "Você é um(a) colega no mesmo time de desenvolvimento e observou essa divergência no GitHub. Qual a atitude mais ética e alinhada ao papel de aliado?",
      opcoes: [
        {
          id: "A",
          texto: "Ficar em silêncio para não gerar 'torta de climão' no time, já que a Mariana é sênior e sabe se defender sozinha se quiser.",
          pontos: 0,
          tipo: "omissao",
          feedback: "A omissão perpetua o ambiente hostil e a sobrecarga emocional das desenvolvedoras. Colegas que não intervêm tornam a desigualdade normalizada."
        },
        {
          id: "B",
          texto: "Intervir no próprio PR com postura técnica acolhedora, validando a alta qualidade dos testes da Mariana e questionando o duplo padrão de exigência com base nas diretrizes do guia de contribuição.",
          pontos: 10,
          tipo: "aliado_proativo",
          feedback: "Excelente! Agir como aliado público desmonta o viés de questionamento constante da competência feminina (prove-it-again bias) e apoia a colega com evidências técnicas."
        },
        {
          id: "C",
          texto: "Aconselhar a Mariana no privado a mudar seu tom e ser mais simpática nas respostas aos comentários para não intimidar os colegas homens.",
          pontos: -5,
          tipo: "culpabilizacao",
          feedback: "Incorreto. Essa resposta transfere a culpa da discriminação para a vítima (tone policing) e perpetua a ideia de que mulheres devem ser agradáveis antes de competentes."
        },
        {
          id: "D",
          texto: "Propor na retrospectiva da sprint a adoção de linters automatizados e um checklist padronizado e cego de Code Review para todo o squad.",
          pontos: 8,
          tipo: "solucao_processo",
          feedback: "Muito bom! Criar critérios objetivos de revisão reduz drasticamente o espaço para vieses inconscientes e subjetividades prejudiciais."
        }
      ],
      fundamentacaoEtica: "Código de Ética ACM/IEEE (Item 1.4): 'Ser justo e agir sem discriminação. A igualdade de tratamento exige que todos os profissionais tenham seu trabalho avaliado por métricas objetivas de engenharia, e não por atributos de gênero ou estereótipos.'",
      dicaAliado: "Se você nota que o código de colegas mulheres recebe muito mais escrutínio do que o de homens com entregas equivalentes, aponte a assimetria com gentileza e baseie os critérios nos padrões oficiais do projeto."
    },
    {
      id: 2,
      titulo: "Daily Scrum & 'Manterrupting' em Arquitetura",
      categoria: "Comunicação & Liderança em Squads Ágeis",
      situacao: "Durante a reunião diária de planejamento de arquitetura de microsserviços, Beatriz (Tech Lead) começa a explicar a estratégia de particionamento de banco de dados. Um desenvolvedor interrompe repetidamente a fala dela antes da conclusão da frase. Minutos depois, ele repete a exata mesma sugestão da Beatriz usando palavras diferentes, e outros colegas parabenizam a ele pela 'ótima ideia'. Além disso, o Scrum Master pede que Beatriz fique encarregada de redigir a ata da reunião.",
      pergunta: "Como você deve intervir para restabelecer o respeito e a autoria técnica da líder?",
      opcoes: [
        {
          id: "A",
          texto: "Interromper a reunião dizendo: 'Pessoal, como a Beatriz acabou de propor há cinco minutos, a ideia original foi dela. Vamos deixá-la concluir a linha de raciocínio de arquitetura.'",
          pontos: 10,
          tipo: "aliado_proativo",
          feedback: "Perfeito! Você combate o 'manterrupting' (interrupção de gênero) e o 'bropropriating' (apropriação de ideias), restaurando a autoridade técnica da líder."
        },
        {
          id: "B",
          texto: "Aceitar que ela faça a ata, afinal mulheres são naturalmente mais organizadas e têm caligrafia melhor.",
          pontos: -10,
          tipo: "estereotipo",
          feedback: "Grave. Atribuir 'trabalho de escritório' e tarefas servis não técnicas (office housework) a engenheiras desvia seu tempo de desenvolvimento e atrasa promoções de carreira."
        },
        {
          id: "C",
          texto: "Esperar a reunião terminar e depois mandar uma mensagem no chat parabenizando a Beatriz pela paciência.",
          pontos: 2,
          tipo: "apoio_passivo",
          feedback: "Embora o apoio moral seja positivo, a intervenção pública no momento do fato é muito mais eficaz para reeducar o comportamento do coletivo."
        },
        {
          id: "D",
          texto: "Propor um rodízio formal entre todos os membros para anotações e atuar como facilitador do tempo de fala.",
          pontos: 7,
          tipo: "solucao_processo",
          feedback: "Boa iniciativa de processo! Rodízio de tarefas burocráticas impede a sobrecarga sistemática das poucas mulheres do time."
        }
      ],
      fundamentacaoEtica: "Princípio 2.3 do Guia SBC de Boas Práticas: 'Fomentar ambientes colaborativos onde a voz de todas as pessoas seja ouvida, combatendo interrupções sistemáticas e garantindo crédito à autoria intelectual.'",
      dicaAliado: "Use a técnica da 'Amplificação': quando uma colega expressar uma ideia importante, repita-a dando o crédito explícito: 'Concordo com a solução que a [Nome] acabou de colocar'."
    },
    {
      id: 3,
      titulo: "Entrevista Técnica e 'Viés de Ajuste Cultural'",
      categoria: "Recrutamento & Seleção em Tecnologia",
      situacao: "Em um comitê de contratação para Engenheiro(a) de Software Pleno, uma candidata mulher com mestrado e vasta experiência em microsserviços recebe nota máxima no teste prático. Na deliberação final, um dos entrevistadores diz: 'Ela é muito boa tecnicamente, mas temos dúvidas sobre o cultural fit. Nosso time joga videogame até tarde e bebe cerveja na sexta, não sei se uma mãe de 32 anos vai se adaptar ao nosso ritmo acelerado'.",
      pergunta: "Qual é a conduta adequada dos membros da banca de seleção?",
      opcoes: [
        {
          id: "A",
          texto: "Concordar com o entrevistador, pois preservar a amizade e o perfil descontraído do squad é mais importante que o teste técnico.",
          pontos: -10,
          tipo: "discriminacao",
          feedback: "Inaceitável. Usar 'fit cultural' como desculpa para contratar apenas pessoas semelhantes ao grupo dominante cria monoculturas e viola a CLT e preceitos éticos."
        },
        {
          id: "B",
          texto: "Pontuar que a avaliação deve ser estritamente pautada nas competências técnicas e comportamentais do cargo, e que critérios familiares e de estilo de vida pessoal são discriminatórios e ilegais.",
          pontos: 10,
          tipo: "aliado_proativo",
          feedback: "Correto! Defender a objetividade nos processos seletivos previne o viés de afinidade e cumpre a legislação trabalhista brasileira (Lei 9.029/95)."
        },
        {
          id: "C",
          texto: "Ligar para a candidata e perguntar informalmente quem cuida dos filhos dela durante a noite antes de decidir.",
          pontos: -10,
          tipo: "ilegalidade",
          feedback: "Totalmente ilegal. Questionamentos sobre estrutura familiar e planejamento reprodutivo são proibidos por lei e violam a privacidade da trabalhadora."
        },
        {
          id: "D",
          texto: "Propor uma segunda entrevista focada apenas em conhecer as preferências de lazer da candidata.",
          pontos: -3,
          tipo: "desvio_foco",
          feedback: "Inadequado. Processos de contratação em Engenharia de Software devem focar na entrega de valor, arquitetura e trabalho em equipe, não na vida pessoal."
        }
      ],
      fundamentacaoEtica: "Meta ODS 5.1 & Código ACM Item 1.4: 'Assegurar igualdade de oportunidades de emprego e remuneração, proibindo discriminação com base em estado civil, parentalidade ou gênero.'",
      dicaAliado: "Estruture entrevistas com matrizes de competência (rubricas cegas) com perguntas idênticas para todos os candidatos, evitando que perguntas subjetivas eliminem mulheres qualificadas."
    },
    {
      id: 4,
      titulo: "Viés Algorítmico & Ética em IA no Hackathon",
      categoria: "Inteligência Artificial & Responsabilidade Social",
      situacao: "Durante uma maratona de desenvolvimento interno, o time de engenharia treina um modelo de triagem de currículos e visão computacional. Joana, desenvolvedora júnior, alerta que o dataset de treino foi extraído dos últimos 10 anos da empresa (em que 90% dos contratados foram homens brancos) e que o modelo está penalizando candidatas mulheres. Dois veteranos dizem 'Deixa isso pra depois, o importante agora é ganhar o pitch com a acurácia global alta'.",
      pergunta: "Qual ação deve ser tomada pelo time de software?",
      opcoes: [
        {
          id: "A",
          texto: "Apoiar o alerta de Joana, demonstrando tecnicamente o viés de dados (sampling bias) e corrigindo a distribuição da base de treino antes de colocar o modelo em produção.",
          pontos: 10,
          tipo: "aliado_proativo",
          feedback: "Excelente! Ética em inteligência artificial requer diversidade e escuta atenta a alertas de impacto social negativo."
        },
        {
          id: "B",
          texto: "Seguir com o modelo enviesado, pois se a matemática diz isso, é porque os homens realmente tinham histórico melhor no mercado.",
          pontos: -10,
          tipo: "falacia_tecnica",
          feedback: "Erro clássico de Machine Learning: 'garbage in, garbage out'. Modelos de IA treinados com dados históricos de exclusão apenas automatizam e ampliam a discriminação."
        },
        {
          id: "C",
          texto: "Pedir para Joana não falar sobre ética durante a apresentação aos jurados para não queimar o projeto.",
          pontos: -8,
          tipo: "censura",
          feedback: "Prejudicial. A engenharia de software contemporânea exige responsabilidade sociotécnica. Omitir falhas éticas gera prejuízos de imagem e multas regulatórias."
        },
        {
          id: "D",
          texto: "Adicionar uma métrica de paridade demográfica (Demographic Parity / Disparate Impact) na pipeline de avaliação do algoritmo.",
          pontos: 8,
          tipo: "solucao_processo",
          feedback: "Muito bom! Métricas quantitativas de justiça algorítmica (Fairness) protegem o sistema contra vieses sistêmicos."
        }
      ],
      fundamentacaoEtica: "Código ACM/IEEE (Item 1.2): 'Evitar causar dano. Sistemas de software não devem perpetuar desigualdades sociais nem discriminação algorítmica.'",
      dicaAliado: "Times diversos produzem software mais seguro e com menos pontos cegos. Valorize as críticas construtivas de colegas de grupos sub-representados."
    },
    {
      id: 5,
      titulo: "Avaliação 360 & O Duplo Padrão de 'Liderança'",
      categoria: "Cultura Organizacional & Promoção",
      situacao: "Na rodada de calibragem de fim de ano para promoção a Staff Engineer, Fernanda e Gabriel lideraram projetos de alta complexidade com entregas impecáveis. Gabriel foi descrito pelo comitê como 'assertivo, visionário e líder nato'. Fernanda, com o mesmo nível de firmeza técnica e negociação de escopo com stakeholders, foi avaliada como 'emocional, difícil de lidar e agressiva na comunicação'.",
      pergunta: "Como agir diante desse nítido duplo padrão de linguagem nas avaliações de desempenho?",
      opcoes: [
        {
          id: "A",
          texto: "Exigir que o comitê compare exemplos concretos de código e entregas de ambos, desconstruindo adjetivos comportamentais enviesados e aplicando critérios objetivos de impacto.",
          pontos: 10,
          tipo: "aliado_proativo",
          feedback: "Brilhante! O duplo padrão linguístico é uma das maiores barreiras para mulheres em cargos sênior. Substituir adjetivos subjetivos por métricas de engenharia elimina a distorção."
        },
        {
          id: "B",
          texto: "Promover apenas o Gabriel para evitar atritos no comitê e sugerir que Fernanda faça um curso de 'inteligência emocional'.",
          pontos: -10,
          tipo: "injustica",
          feedback: "Perpetua a injustiça. Penaliza a mulher por demonstrar a mesma firmeza que é elogiada nos homens."
        },
        {
          id: "C",
          texto: "Reconhecer que homens e mulheres têm estilos diferentes e que cabe à mulher se adaptar à sensibilidade do comitê.",
          pontos: -6,
          tipo: "conformismo",
          feedback: "Equivocado. Uma cultura de engenharia inclusiva não exige que mulheres adotem estereótipos de submissão para serem aceitas."
        },
        {
          id: "D",
          texto: "Implementar diretrizes corporativas que banem o uso de palavras de viés de gênero nos relatórios oficiais de RH e Engenharia.",
          pontos: 8,
          tipo: "solucao_processo",
          feedback: "Excelente! Empresas inovadoras utilizam filtros de texto para barrar avaliações 360 baseadas em estereótipos de gênero."
        }
      ],
      fundamentacaoEtica: "Meta ODS 5.5: 'Garantir oportunidades iguais para a liderança técnica e tomadas de decisão'.",
      dicaAliado: "Preste atenção aos adjetivos: quando uma colega for chamada de 'mandona' ou 'agressiva', pergunte a si mesmo: 'Se um homem fizesse exatamente isso, ele seria elogiado como determinado?'"
    }
  ],

  pioneirasTech: [
    {
      nome: "Ada Lovelace",
      periodo: "1815 - 1852",
      titulo: "Primeira Programadora da História",
      contribuicao: "Escreveu o primeiro algoritmo destinado a ser processado por uma máquina (a Máquina Analítica de Babbage), prevendo que computadores manipulariam não apenas números, mas símbolos e música.",
      legado: "Pioneira dos fundamentos conceituais do software."
    },
    {
      nome: "Margaret Hamilton",
      periodo: "1936 - presente",
      titulo: "Diretora do Software da Apollo 11",
      contribuicao: "Cunhou o termo 'Engenharia de Software' para exigir rigor científico para o código. Liderou a equipe do MIT que desenvolveu o software de voo da missão lunar, salvando o pouso com priorização de tarefas.",
      legado: "Mãe da Engenharia de Software e da tolerância a falhas."
    },
    {
      nome: "Grace Hopper",
      periodo: "1906 - 1992",
      titulo: "Criadora do Compilador e do COBOL",
      contribuicao: "Almirante da Marinha dos EUA, concebeu o primeiro compilador da história e liderou a criação da linguagem COBOL, provendo linguagens legíveis por humanos no lugar de código binário puro.",
      legado: "Popularizou o termo 'debugging' e revolucionou linguagens de alto nível."
    },
    {
      nome: "Claudia Bauzer Medeiros",
      periodo: "1954 - presente",
      titulo: "Pioneira Brasileira & Pesquisadora da Unicamp",
      contribuicao: "Referência mundial em Ciência de Dados, e-Science e Bancos de Dados Complexos. Uma das grandes líderes da SBC na criação de políticas de inclusão de mulheres na computação no Brasil.",
      legado: "Defensora ativa da diversidade na pós-graduação e pesquisa científica."
    }
  ],

  checklistBoasPraticas: [
    {
      titulo: "Revisão de Código Ética e Objetiva",
      descricao: "Use checklists pré-definidos com linters automatizados; avalie arquitetura, testes e lógica, evitando suposições de incapacidade técnica."
    },
    {
      titulo: "Interrupção Zero em Reuniões Técnicas",
      descricao: "Estabeleça a regra de não interromper quem estiver com a palavra. Se presenciar interrupção de colegas mulheres, intervenha de forma assertiva."
    },
    {
      titulo: "Amplificação de Ideias & Crédito Intelectual",
      descricao: "Ao concordar com uma proposta, cite explicitamente a autora original da ideia, evitando apropriações acidentais ou intencionais."
    },
    {
      titulo: "Rodízio Justo de Tarefas Não Técnicas",
      descricao: "Anotação de atas, agendamento de salas e organização de eventos da sprint devem ser revezados entre todas as pessoas do time, sem recair apenas sobre mulheres."
    },
    {
      titulo: "Processos Seletivos com Critérios Cegos",
      descricao: "Avalie desafios técnicos de forma anônima e proíba qualquer questionamento sobre vida privada, estado civil, filhos ou planos de gravidez."
    },
    {
      titulo: "Mentoria Ativa e Patrocínio de Carreira (Sponsorship)",
      descricao: "Engenheiros sêniores e gestores devem atuar ativamente no apadrinhamento de desenvolvedoras, abrindo portas para projetos críticos de arquitetura."
    }
  ]
};
