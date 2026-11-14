# Contrato do mock sintético

## Finalidade

Fornecer três arquivos de entrada coerentes para o projeto de previsão da demanda do RU. A decisão pretendida é estimar, na véspera, a quantidade de refeições do dia seguinte por tipo para o RU inteiro; curso é um detalhamento. O valor em R$ poderá ser calculado posteriormente a partir da quantidade e de um preço de referência. O gerador atual não calcula valores monetários.

## Arquivos, grão e chaves

| Arquivo | Uma linha representa | Chave |
|---|---|---|
| `catraca_ru.csv` | Uma tentativa de acesso ao RU | `id_registro_utilizacao` |
| `estudantes.csv` | Um vínculo acadêmico em um período letivo | `id_matricula, periodo_letivo` |
| `matriculas_componentes.csv` | Uma inscrição em componente/turma no período | `id_matricula_componente` |

`id_matricula` liga os acessos e os componentes ao vínculo acadêmico; `id_discente` identifica o estudante e pode ter mais de um vínculo. A data do evento determina o período da catraca. Todos os identificadores são fictícios e devem ser lidos como texto.

## Cobertura e regras de geração

- Período simulado: **01/01/2019 a 14/11/2026**, fixo para reprodução; uma unidade fictícia e seis cursos técnicos fictícios.
- A semente `20261001` fixa a geração. O script cria cadastro por período, três inscrições em componentes por vínculo ativo e tentativas de acesso de segunda a sábado.
- A probabilidade de tentativa varia artificialmente conforme refeição, aula prevista e residência estudantil. As tentativas são classificadas como `servida` ou `negada`; o modo de processamento é `automatica` ou `manual`.
- O calendário simplifica os períodos letivos, recessos e suspensões. Faltas e notas são consolidadas por componente e período.
- A catraca contém tentativas negadas para que uma análise posterior distinga acessos de refeições efetivamente servidas.

Essas regras são **hipóteses da simulação**, não padrões medidos no CAVN/UFPB. Os três CSVs são gerados pelo único script do projeto. A definição de cada campo e das categorias está em [dicionario_mock.md](dicionario_mock.md).

## Limites

O mock não informa demanda real, custo efetivo, elegibilidade para auxílio ou desempenho de um modelo. O formato exato dos arquivos institucionais permanece desconhecido. Se chegarem, as chaves, categorias e datas terão de ser conferidas antes de qualquer integração.
