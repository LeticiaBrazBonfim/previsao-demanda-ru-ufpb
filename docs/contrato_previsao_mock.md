# Contrato do mock sintético

## Finalidade

Fornecer três arquivos de entrada coerentes para o projeto de previsão da demanda do RU. A decisão pretendida é estimar, na véspera, a quantidade de refeições do dia seguinte **por tipo e por curso**. O total do RU é a soma dos cursos. O gerador atual não contém valores monetários.

## Arquivos, grão e chaves

| Arquivo | Uma linha representa | Chave |
|---|---|---|
| `catraca_ru.csv` | Uma tentativa de acesso ao RU | `id_registro_utilizacao` |
| `estudantes.csv` | Um vínculo acadêmico em um período letivo | `id_matricula, periodo_letivo` |
| `matriculas_componentes.csv` | Uma inscrição em componente/turma no período | `id_matricula_componente` |

`id_matricula` liga os acessos e os componentes ao vínculo acadêmico; `id_discente` identifica o estudante e pode ter mais de um vínculo. A data do evento permite procurar um período letivo vigente, mas alguns acessos do mock ocorrem fora dos intervalos letivos e não devem receber um período falso. Todos os identificadores são fictícios e devem ser lidos como texto.

## Cobertura e regras de geração

- Período simulado: **01/01/2019 a 14/11/2026**, fixo para reprodução; uma unidade fictícia e seis cursos técnicos fictícios.
- A semente `20261001` fixa a geração. O script cria cadastro por período, três inscrições em componentes por vínculo ativo e tentativas de acesso de segunda a sábado.
- A probabilidade de tentativa varia artificialmente conforme refeição, aula prevista e residência estudantil. As tentativas são classificadas como `servida` ou `negada`; o modo de processamento é `automatica` ou `manual`.
- O calendário simplifica os períodos letivos, recessos e suspensões. Faltas e notas são consolidadas por componente e período.
- A catraca contém tentativas negadas para que uma análise posterior distinga acessos de refeições efetivamente servidas.

Essas regras são **hipóteses da simulação**, não padrões medidos no CAVN/UFPB. Os três CSVs são gerados pelo único script do projeto. A definição de cada campo e das categorias está em [dicionario_mock.md](dicionario_mock.md).

## Limites

O mock não informa demanda real, custo efetivo, elegibilidade para auxílio ou desempenho de um modelo. O formato exato dos arquivos institucionais permanece desconhecido. Se chegarem, as chaves, categorias e datas terão de ser conferidas antes de qualquer integração.

## Contrato analítico da Entrega 04

- **Unidade e alvo principais:** uma data × um tipo de refeição × um curso para o RU simulado; `quantidade_servida` é o número de IDs distintos de catraca com `situacao_evento = servida`. O total secundário por data/refeição é a soma dos cursos com cobertura completa.
- **Corte da decisão:** fim do dia anterior ao previsto (`D-1`), supondo que os eventos até esse instante já estejam disponíveis. Calendário e tipo de refeição são conhecidos; eventos de `D`, notas e faltas consolidadas não são entradas válidas. A disponibilidade e a frequência de atualização reais da catraca e do cadastro ainda não foram confirmadas.
- **Cobertura e população:** 01/01/2019 a 14/11/2026, uma unidade e cursos técnicos inteiramente fictícios. O gerador fixa essa cobertura e usa a semente `20261001`; sua reprodução não equivale a uma atualização institucional.
- **Dias sem eventos:** o gerador simula abertura de segunda a sábado, cobertura completa em todo o período e os mesmos seis cursos ativos. Por isso, uma combinação sem evento no mock é zero conhecido. As métricas principais usam apenas dias abertos. Para dados reais, a base `cobertura_real.csv` deve listar data, refeição, curso ativo, abertura e integridade da extração. Uma combinação sem extração completa recebe alvo vazio e fica fora da avaliação; o notebook não inventa zeros.
- **Restrições:** os CSVs são públicos apenas por serem inteiramente sintéticos. Não permitem inferir demanda real, custo contábil, saldo para subsídios nem elegibilidade individual. O cruzamento com dados reais exigirá chaves confiáveis, autorização e revisão de privacidade.
- **Valor em R$:** não existe preço nem valor observado no mock. A Entrega 3 cita aproximadamente R$ 16 por refeição como hipótese, sem comprovação de vigência ou correspondência ao custo real. A base por curso deixa `valor_observado` vazio no mock. Se o dado real contiver **um valor monetário por evento servido**, a equipe poderá configurar o nome da coluna após conferir sua semântica e unidade; o notebook somará esses valores por data/refeição/curso. Preço cobrado, custo contratual e subsídio devem ser distinguidos antes de calcular qualquer cenário financeiro.

## Adaptação ao dado real

Trocar a pasta de entrada não basta. É preciso mapear colunas, verificar chaves e categorias, ajustar os cortes temporais, confirmar a completude de cada extração e fornecer `cobertura_real.csv` com `data`, `tipo_refeicao`, `curso`, `aberto` e `extracao_completa` (`sim`/`nao`). O arquivo deve conter só cursos ativos em cada data. Sem essa evidência, a ausência de evento não pode ser tratada como consumo zero. A regra de planejamento vigente no RU, sua capacidade e seus custos também permanecem sem confirmação.
