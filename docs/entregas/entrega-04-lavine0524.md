Relatório Individual — Entrega 04
1. Identificação
Nome: Bianca Lavine
Usuário GitHub: lavine0524
Número da Entrega: Entrega 04 (Base analítica, pré-processamento e baseline)
Branch Utilizada: entrega-04-lavine0524
Repositório: LeticiaBrazBonfim/previsao-demanda-ru-ufpb
2. Atividades Realizadas
Configuração do ambiente virtual Python (.venv) e instalação controlada das dependências declaradas no requirements.txt (numpy, pandas, python-dateutil, tzdata).
Leitura e auditoria dos arquivos brutos do mock (catraca_ru.csv, estudantes.csv e matriculas_componentes.csv) localizados em dados/bruto/mock/.
Filtragem rigorosa dos eventos de catraca para considerar apenas as refeições com situacao_evento == "servida", preservando o grão unitário do evento (id_registro_utilizacao).
Associação temporal dos eventos de catraca com os períodos letivos da tabela de estudantes, utilizando a verificação de vigência (between(inicio_periodo_letivo, fim_periodo_letivo)).
Agrupamento e agregação dos dados de componentes curriculares por matrícula e período letivo para evitar duplicações e estouros de memória (MemoryError).
Construção da base analítica diária agregada por data e tipo de refeição, complementando a grade temporal completa para cobrir todas as combinações (8.625 linhas equivalentes a 2.875 dias  3 tipos de refeição), preenchendo as ausências com zero.
Salvamento da base processada em dados/processado/base_analitica_diaria.csv.
3. Arquivos Criados ou Modificados
docs/entregas/entrega-04-lavine0524.md (Este relatório individual).
dados/processado/base_analitica_diaria.csv (Base analítica diária gerada e completa).
Notebook de exploração e auditoria na pasta notebooks/.
4. Metodologia
A metodologia adotada priorizou a integridade dos dados e a reprodutibilidade, seguindo as diretrizes do projeto:
Preservação do Grão: Cada refeição servida única foi identificada por seu id_registro_utilizacao, garantindo que cruzamentos com tabelas 1-para-muitos (como componentes curriculares) não multiplicassem artificialmente a contagem de demanda.
Associação Temporal: Os eventos de catraca foram validados contra o intervalo letivo dos discentes. Os registros sem período letivo formal correspondente (15.777 eventos) foram investigados, observando-se que se concentram em janeiro, julho e dezembro, sendo mantidos na contagem total de demanda para evitar descarte indevido.
Grade Completa: A base foi expandida para uma grade cartesiana contínua de datas e tipos de refeição, garantindo consistência temporal para os modelos preditivos subsequentes.
5. Testes e Verificações
Contagem Bruta vs. Filtrada: Confirmação de 221.600 eventos servidos a partir de um total bruto de 224.880 registros na catraca (sendo 3.280 eventos negados).
Validação de Unicidade: Verificação de que o identificador de evento único não apresentou duplicidades.
Checagem de Soma Total: Auditoria rigorosa garantindo que o total de refeições agregadas na base diária permaneceu exatamente em 221.600, tanto antes quanto após a complementação da grade temporal com zeros.
6. Resultados
Foram mantidos os 221.600 eventos classificados como servidos.
A associação temporal com os períodos letivos encontrou correspondência exata para 205.823 eventos; 15.777 não tiveram período letivo formal compatível, concentrando-se em janeiro, julho e dezembro. Esse padrão é compatível com períodos de recesso ou transição letiva no mock, mas a correspondência com os intervalos individuais de recesso ainda precisa ser confirmada.
A base foi agregada por data e tipo de refeição e completada para 2.875 datas  3 refeições, totalizando 8.625 linhas. As combinações sem eventos foram preenchidas com zero, preservando integralmente o total de 221.600 refeições servidas.
A base processada encontra-se salva localmente no caminho dados/processado/base_analitica_diaria.csv.
7. Limitações e Pendências
O mock é sintético. Ainda é necessário confirmar, com o contrato dos dados ou as regras de geração, se os eventos sem período letivo correspondem a refeições registradas durante recessos.
Com a base analítica consolidada e validada, a equipe está apta a prosseguir para a próxima etapa da Entrega 5 (modelagem de baselines e métricas de avaliação).

