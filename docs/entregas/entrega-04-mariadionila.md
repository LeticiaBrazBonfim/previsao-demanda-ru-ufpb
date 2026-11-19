# Entrega 04: Maria Dionila

## Identificação

- Integrante: Maria Dionila
- Usuário GitHub: mariadionila
- Entrega: 04
- Branch: `entrega-04-mariadionila`

## Atividades realizadas

Implementei um baseline operacional e um baseline trivial sobre a base diária do RU, medi a métrica na validação temporal e expliquei os erros por tipo de refeição e no total. Também converti o erro em R$ a partir de um preço de referência documentado, e registrei pressupostos, limitações e comparação entre os dois baselines.


## Arquivos criados ou modificados

- `notebooks/individuais/entrega-04-mariadionila.ipynb`: notebook executável do início ao fim. Reproduz a base diária (grão `data × tipo_refeicao`) e a partição temporal (treino/validação/teste) como pré-requisito, e contém a seção de baselines: cálculo do baseline trivial e do operacional, métrica na validação, erro em R$, tabela de resultados, explicação dos erros, pressupostos/limitações e diagnóstico de vazamento de três variáveis.
- `docs/entregas/entrega-04-mariadionila.md`: este relatório.
- `dados/processado/base_analitica_diaria.csv` e `dados/processado/resultados_baselines_validacao.csv`: gerados pela execução do notebook (não versionados, conforme `.gitignore` do projeto).

## Metodologia

- **Base diária** (reprodução): apenas eventos `servida` de `catraca_ru.csv`, contados por `data` e `tipo_refeicao`, com a grade completa de datas preenchida com zero nos dias sem evento (inclusive domingos, em que o RU simulado não abre). Reconciliei a soma da base agregada com o total de eventos servidos (221.600).
- **Partição temporal** (reprodução dos cortes de Kaio Vitor): treino de 01/01/2019 a 31/12/2024 (2.192 dias), validação de 01/01/2025 a 31/12/2025 (365 dias), teste de 01/01/2026 a 14/11/2026 (318 dias), sem sobreposição. O teste não foi usado nesta seção.
- **Baseline trivial**: média da `quantidade_servida` no treino, por tipo de refeição, aplicada como previsão constante em todos os dias da validação.
- **Baseline operacional**: defasagem de 7 dias (`t-7`) — a quantidade servida na mesma data da semana anterior é usada como previsão para o dia atual. Representa a regra que, na prática, orienta a fila hoje, sem qualquer modelo, e usa apenas informação disponível até o fim da véspera.
- **Métrica**: MAE (erro absoluto médio) como métrica principal, com MAPE e RMSE como leituras complementares, calculados por tipo de refeição e no total, no recorte de validação. Dias com demanda real igual a zero entram no MAE e no RMSE, mas ficam fora da média do MAPE (indefinida quando o real é zero), e esses dias foram contados à parte.
- **R$**: `quantidade × preço de referência`, com preço de referência ilustrativo de R$ 2,00 por refeição (o mock não contém preços; o valor está documentado no notebook e não é um preço oficial do RU/UFPB).

## Testes e verificações

Criei um ambiente virtual próprio (`.venv`, Python 3.12.10) e instalei as dependências já declaradas em `requirements.txt` (`pandas==3.1.0`, `numpy==2.5.4`). Rodei o notebook do início ao fim com o kernel reiniciado (`jupyter nbconvert --execute`), sem intervenção manual e sem caminhos absolutos de outra máquina. Conferi:

- A reconciliação da base diária (soma agregada igual ao total de eventos servidos: 221.600).
- A partição temporal em ordem e sem sobreposição (treino < validação < teste).
- Que todas as linhas da validação tiveram defasagem de 7 dias disponível (0 linhas sem `previsto_operacional`).
- Que a tabela de resultados final foi salva em `dados/processado/resultados_baselines_validacao.csv`.


## Resultados

Métrica na validação temporal (01/01/2025 a 31/12/2025), por tipo de refeição e no total:

| Baseline | Tipo de refeição | MAE | RMSE | MAPE (%) | MAE em R$ |
|---|---|---:|---:|---:|---:|
| Trivial | Almoço | 26,75 | 27,72 | 94,5 | 53,50 |
| Trivial | Café da manhã | 13,19 | 14,20 | 70,9 | 26,37 |
| Trivial | Jantar | 10,94 | 12,10 | 57,4 | 21,88 |
| Trivial | **Total** | **16,96** | **19,29** | **74,2** | **33,92** |
| Operacional (t-7) | Almoço | 7,76 | 14,14 | 33,7 | 15,53 |
| Operacional (t-7) | Café da manhã | 5,30 | 8,06 | 35,2 | 10,60 |
| Operacional (t-7) | Jantar | 5,07 | 7,45 | 32,7 | 10,14 |
| Operacional (t-7) | **Total** | **6,04** | **10,33** | **33,9** | **12,09** |

O baseline operacional supera o trivial em todas as métricas, por tipo de refeição e no total: MAE total cai de 16,96 para 6,04, e MAPE total cai de 74,2% para 33,9%. Em R$ (a R$ 2,00/refeição), o erro diário somado nas três refeições fica em torno de R$ 36 (operacional) contra R$ 102 (trivial) — a régua para um futuro modelo se justificar.

- A média constante do trivial ignora o padrão semanal (inclusive domingo fechado); a defasagem de 7 dias captura esse padrão, daí a maior parte do ganho.
- Almoço tem o maior MAE absoluto nos dois baselines, por ter a maior quantidade média servida; no MAPE, as três refeições ficam próximas, porque erros menores pesam proporcionalmente mais sobre quantidades menores.
- O operacional ainda carrega o crescimento da demanda ao longo do tempo (Kaio Vitor: teste ~14% acima do treino) e tende a ficar abaixo do real em períodos de crescimento, por usar só o valor de 7 dias atrás.

## Limitações e pendências

- Os cortes da partição (31/12/2024 e 31/12/2025) são os mesmos propostos por Kaio Vitor e seguem provisórios, sujeitos a confirmação do grupo.
- O preço de referência de R$ 2,00 por refeição é um pressuposto documentado para fins didáticos, não um preço oficial do RU/UFPB; o mock não contém preços.
- Os dois baselines são simples por definição e não usam variáveis de calendário, vínculo ou auxílio; um modelo posterior pode reduzir ainda mais o erro usando essas informações, desde que respeite a classificação de vazamento.
- Não avaliei o conjunto de teste, conforme a regra de só usá-lo na avaliação final.
- Os dados são inteiramente sintéticos; os valores de erro e de R$ não representam desempenho esperado com dados reais do RU/UFPB.

## Diagnóstico de vazamento (verificação individual)

Três variáveis relacionadas à construção dos baselines, classificadas em relação ao corte no fim do dia `D-1`:

- **Permitida**: `quantidade_servida` em `D-7` (defasagem de 7 dias, usada no baseline operacional). Já aconteceu e foi registrada muito antes do fim de `D-1`; não usa nenhuma informação do dia previsto.
- **Proibida por vazamento temporal**: `quantidade_servida` do próprio dia `D`. É o alvo da previsão; só existe depois que o dia `D` termina e as refeições já foram servidas.
- **Proibida por consequência da decisão**: quantidade de tentativas negadas (`situacao_evento = negada`) no dia `D`. Negadas em `D` podem ocorrer porque a quantidade preparada seguiu o baseline e foi insuficiente. Usá-las para corrigir o próprio baseline faria ele aprender o efeito da sua decisão anterior, não a demanda real.

## Uso de IA generativa

Usei o Claude como apoio para organizar a seção de baselines do notebook, redigir as explicações em markdown e revisar o cálculo das métricas e deste relatório.
