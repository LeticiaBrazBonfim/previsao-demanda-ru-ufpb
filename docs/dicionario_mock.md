# Dicionário do mock sintético

## Cobertura e formato

- Período simulado: **01/01/2019 a 14/11/2026**. A data final é fixa no script para reprodução.
- Arquivos: CSV em UTF-8, separador vírgula, cabeçalho na primeira linha.
- Datas: `AAAA-MM-DD`; data e hora: `AAAA-MM-DD HH:MM:SS`; horários: `HH:MM`; período letivo: `AAAA.1` ou `AAAA.2`.
- Identificadores, inclusive `matricula`, devem ser lidos como **texto**. A matrícula tem zeros à esquerda após o ano.
- Todas as pessoas, aulas, calendários, acessos, auxílios e situações são fictícios. O mock não contém preços.

Três arquivos físicos concentram as seis tabelas acadêmicas conceituais pedidas: `estudantes.csv` reúne Discentes, Curso/Matriz/Currículo, SituaçãoDiscentesPeriodos e calendário; `matriculas_componentes.csv` reúne Componentes, Docentes, matrículas em componentes e horários; `catraca_ru.csv` contém os eventos de utilização. A repetição de dados de curso e calendário é deliberada para manter três CSVs.

Essa compactação é uma **exceção de finalidade didática** ao princípio de manter cada tipo de observação em uma tabela. As chaves e os grãos abaixo tornam as repetições explícitas. Se a extração institucional chegar em seis ou mais arquivos, os originais deverão ser preservados e mapeados após conferência; não se deve pressupor cabeçalhos idênticos.

## catraca_ru.csv

**Grão:** uma tentativa de acesso por linha, servida ou negada. **Chave primária:** `id_registro_utilizacao`. **Chave estrangeira:** `id_matricula` para `estudantes.csv`; o período correspondente é determinado pela data do evento.

| Campo | Descrição |
|---|---|
| `id_registro_utilizacao` | ID único do evento |
| `unidade_ru` | Restaurante/unidade: `RU_CAVN_SIMULADO` |
| `tipo_refeicao` | `cafe_da_manha`, `almoco` ou `jantar` |
| `tipo_acesso` | `total` ou `parcial`; não há outras categorias nesta simulação |
| `data_hora_refeicao` | Data e hora da tentativa |
| `tipo_liberacao` | `automatica` ou `manual`; indica como a tentativa foi processada |
| `nivel_ensino` | `tecnico` |
| `matricula` | Número fictício de matrícula, texto |
| `id_matricula` | ID do vínculo acadêmico, texto; preserva vínculos múltiplos |
| `curso` | Nome fictício do curso |
| `id_curso` | ID fictício do curso |
| `tipo_auxilio` | `residencia_estudantil`, `auxilio_alimentacao` ou `sem_auxilio` |
| `situacao_evento` | `servida` ou `negada`; somente `servida` entra no alvo |

## estudantes.csv

**Grão:** um vínculo acadêmico por período letivo. **Chave primária composta:** `id_matricula, periodo_letivo`. Um `id_discente` pode ter mais de um `id_matricula`; o vínculo não é fundido. Curso, matriz e currículo são atributos repetidos nesse grão.

| Campo | Descrição |
|---|---|
| `id_discente` | ID fictício do estudante |
| `id_matricula` | ID fictício do vínculo |
| `matricula` | Número fictício do vínculo como texto |
| `id_curso`, `curso` | Identificador e nome do curso |
| `nivel_ensino` | `tecnico` |
| `id_matriz` | Identificador da matriz curricular |
| `id_curriculo` | Identificador do currículo |
| `periodo_ingresso` | Período de ingresso do vínculo |
| `periodo_letivo` | Período a que esta linha se refere |
| `situacao_vinculo_periodo` | `ativo`, `trancado`, `cancelado` ou `concluido` |
| `inicio_periodo_letivo`, `fim_periodo_letivo` | Datas do calendário acadêmico simulado |
| `inicio_recesso`, `fim_recesso` | Recesso anterior ao período letivo |
| `datas_suspensao_atividades` | Uma data de suspensão simulada por período |
| `residente` | Indicador fictício de residência estudantil |
| `tipo_auxilio` | Categorias descritas para a catraca |

## matriculas_componentes.csv

**Grão:** uma matrícula de vínculo em componente/turma por período. **Chave primária:** `id_matricula_componente`. **Chave estrangeira composta:** `id_matricula, periodo_letivo` para `estudantes.csv`.

| Campo | Descrição |
|---|---|
| `id_matricula_componente` | ID único desta inscrição |
| `id_matricula`, `periodo_letivo` | Vínculo e período |
| `id_componente`, `componente` | Identificador e nome do componente curricular |
| `id_turma` | Identificador da turma |
| `dias_semana_aula` | Dias previstos, separados por `|`; códigos: SEG, TER, QUA, QUI, SEX |
| `horario_inicio`, `horario_fim` | Horários programados |
| `modalidade` | `presencial` ou `hibrida` |
| `local_aula` | Sala ou laboratório fictício |
| `id_docente`, `docente` | Identificador e descrição fictícia do docente |
| `aulas_previstas` | Aulas previstas no componente/período |
| `faltas` | Faltas **consolidadas** no componente/período |
| `frequencia_percentual` | `100 × (aulas_previstas - faltas) / aulas_previstas` |
| `nota_final` | Nota final fictícia, escala 0–10 |
| `resultado_final` | `aprovado` ou `reprovado` |

## Correspondência com a solicitação

| Solicitação | Local no mock |
|---|---|
| Evento de RU com ID, unidade, refeição, acesso, data/hora, liberação, nível, matrícula, vínculo, curso, auxílio e situação | `catraca_ru.csv`, campos homônimos acima |
| Discentes; curso, matriz e currículo; ingresso; situação por período | `estudantes.csv` |
| Componentes; docentes; matrícula em componente, turma e período | `matriculas_componentes.csv` |
| Dias, horários, modalidade e local da aula | `matriculas_componentes.csv` |
| Frequência/faltas | `matriculas_componentes.csv`, **consolidadas por componente/período** |
| Notas e resultados finais | `matriculas_componentes.csv` |
| Início/fim letivo, recessos e suspensão | `estudantes.csv`, repetidos por vínculo/período |
| Ligação por `id_matricula` e vínculos múltiplos | Os três CSVs; `id_discente` identifica o estudante sem fundir vínculos |

## Limitações conhecidas

- O mock não contém frequência por **data de aula**; usa a opção consolidada indicada na solicitação.
- O mock não gera cancelamentos. Se uma extração real trouxer essa situação, preservar a categoria original e documentar sua definição.
- O calendário é simplificado: um recesso anterior e uma data de suspensão por período, sem feriados reais. O RU simulado abre de segunda a sábado. Horários e presença são programados, não observados.
- Os seis conjuntos acadêmicos pedidos foram comprimidos em duas tabelas largas. Não são extrações reais dessas tabelas.
- Não há preço por refeição nem histórico de preços nos CSVs do mock.
- A simulação não permite inferir demanda, frequência, custo ou comportamento reais do CAVN/UFPB.
- Dicionários públicos da [UFRN para discentes](https://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/b5144c99-81f3-4cfc-8938-18adb81ae3c0/download/discentesdicionario.pdf) e da [UFS para turmas](https://dados.ufs.br/dataset/turmas/resource/dicionario-de-dados---turmas-da-ufs/download/dicionario-de-dados-turmas-da-ufs.pdf) mostram que a matrícula pode ter nome diferente de `id_matricula` e que o horário pode vir como texto codificado. Esses exemplos não definem o esquema da UFPB. Sem chave de correspondência confiável, o cruzamento entre RU e dados acadêmicos fica pendente.
