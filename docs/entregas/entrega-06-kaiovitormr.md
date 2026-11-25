# Entrega 06 — Contribuição individual

**Integrante:** Kaiovitormr
**Projeto:** Previsão de demanda do RU/UFPB  
**Branch:** entrega-06-kaiovitormr

## 8. Análise de erros e equidade

### 8.1 Metodologia

A contribuição individual teve como objetivo analisar os erros de previsão e identificar diferenças de desempenho entre os grupos presentes na base de dados.

Foram desenvolvidas funções para:

- Calcular o erro individual das previsões;
- Calcular MAE, RMSE e viés;
- Identificar subestimações e superestimações;
- Comparar erros por curso e tipo de refeição;
- Analisar erros por período e faixa de demanda;
- Identificar casos críticos;
- Avaliar diferenças de desempenho entre grupos.

Foi adotado um mínimo exploratório de 30 observações por grupo como referência de suficiência amostral, sem garantia de representatividade estatística.

As funções foram desenvolvidas no notebook:

`notebooks/individuais/entrega-06-kaiovitormr.ipynb`

### 8.2 Diagnóstico da base mock

A base analítica utilizada possui 51.750 registros, dos quais 44.370 correspondem a períodos de funcionamento do RU e 7.380 a períodos de fechamento.

| Indicador | Resultado |
|---|---:|
| Total de registros | 51.750 |
| Registros com RU aberto | 44.370 |
| Registros com RU fechado | 7.380 |
| Cobertura da extração no mock | 100% |
| Registros duplicados | 0 |
| Demandas negativas | 0 |
| Refeições servidas com RU fechado | 0 |

A variável `quantidade_servida` não apresenta valores ausentes e foi utilizada como alvo, conforme o contrato do projeto.

A coluna `valor_observado` apresenta valores ausentes em todos os registros e, por esse motivo, não foi utilizada como alvo da análise.

### 8.3 Análise da demanda por refeição

| Refeição | Registros com RU aberto | Total servido | Média | Desvio padrão |
|---|---:|---:|---:|---:|
| Almoço | 14.790 | 110.161 | 7,45 | 4,42 |
| Café da manhã | 14.790 | 58.707 | 3,97 | 2,68 |
| Jantar | 14.790 | 52.732 | 3,57 | 2,46 |
| Total | 44.370 | 221.600 | - | - |

O almoço concentra aproximadamente 49,71% das refeições servidas na base simulada. Além de apresentar a maior demanda média, também possui o maior desvio padrão.

Esse comportamento indica uma maior variabilidade absoluta na quantidade de refeições servidas, sendo importante considerar essa característica durante a análise dos erros de previsão.

### 8.4 Análise da demanda por curso

| Curso | Registros | Total de refeições | Demanda média | Desvio padrão |
|---|---:|---:|---:|---:|
| Curso A | 7.395 | 28.629 | 3,87 | 3,50 |
| Curso B | 7.395 | 45.480 | 6,15 | 3,63 |
| Curso C | 7.395 | 28.454 | 3,85 | 3,53 |
| Curso D | 7.395 | 45.426 | 6,14 | 3,65 |
| Curso E | 7.395 | 28.169 | 3,81 | 3,44 |
| Curso F | 7.395 | 45.442 | 6,14 | 3,60 |

Os cursos B, D e F apresentam demandas médias superiores às dos cursos A, C e E.

Apesar de todos os cursos possuírem a mesma quantidade de registros, existem diferenças no volume de refeições consumidas. Dessa forma, a avaliação dos erros deve considerar as particularidades de cada grupo.

### 8.5 Análise preliminar dos erros

Para realizar uma análise inicial, foram utilizadas as métricas dos baselines anteriores, disponíveis no arquivo:

`dados/processado/resultados_baselines_validacao_por_curso.csv`

Foram avaliados dois métodos:

- Média do treino;
- D-7 proposto.

Cada método possui 18 grupos de análise, correspondentes às combinações entre seis cursos e três tipos de refeição, com 313 observações por grupo.

As métricas consolidadas foram calculadas considerando a quantidade de observações de cada grupo. O MAE foi ponderado pelo número de registros, enquanto o RMSE foi obtido pela raiz da média ponderada dos valores de RMSE ao quadrado.

Como as métricas originais podem estar arredondadas, os resultados consolidados são aproximações.

#### Erros consolidados por curso

| Curso | Observações por método | MAE D-7 | RMSE D-7 | MAE média do treino | RMSE média do treino |
|---|---:|---:|---:|---:|---:|
| A | 939 | 1,94 | 2,79 | 2,61 | 3,15 |
| B | 939 | 2,34 | 3,09 | 2,78 | 3,35 |
| C | 939 | 1,96 | 2,80 | 2,64 | 3,21 |
| D | 939 | 2,35 | 3,15 | 2,75 | 3,34 |
| E | 939 | 1,94 | 2,73 | 2,53 | 3,10 |
| F | 939 | 2,30 | 3,11 | 2,70 | 3,28 |

O D-7 apresentou menor MAE em todos os cursos avaliados.

Nesse método, o curso D apresentou o maior MAE consolidado, com 2,35 refeições por observação, enquanto os cursos A e E apresentaram os menores valores, ambos com aproximadamente 1,94.

#### Erros consolidados por refeição

| Refeição | Observações por método | MAE D-7 | RMSE D-7 | MAE média do treino | RMSE média do treino |
|---|---:|---:|---:|---:|---:|
| Almoço | 1.878 | 2,56 | 3,55 | 3,98 | 4,45 |
| Café da manhã | 1.878 | 2,01 | 2,68 | 2,13 | 2,56 |
| Jantar | 1.878 | 1,85 | 2,51 | 1,89 | 2,27 |

O almoço apresentou os maiores valores de MAE nos dois métodos analisados.

A utilização do D-7 apresentou uma redução aproximada de 35,68% no MAE do almoço em comparação com a média do treino.

Entretanto, o RMSE do D-7 foi superior no café da manhã e no jantar, mostrando que a redução do erro absoluto médio não representa necessariamente uma melhora em todos os indicadores.

### 8.6 Comparação entre grupos

| Indicador | D-7 proposto | Média do treino |
|---|---:|---:|
| Grupos avaliados | 18 | 18 |
| Observações por método | 5.634 | 5.634 |
| Menor MAE | 1,52 | 1,73 |
| Maior MAE | 2,80 | 4,11 |
| Diferença entre extremos | 1,28 | 2,38 |
| Diferença percentual | 84,21% | 137,57% |

No D-7, o maior erro foi identificado no almoço do curso D, com MAE de 2,80 refeições. O menor erro ocorreu no jantar do curso A, com MAE de 1,52.

Na média do treino, o maior erro ocorreu no almoço do curso B, com MAE de 4,11, enquanto o menor ocorreu no jantar do curso E, com MAE de 1,73.

O D-7 apresentou uma menor diferença entre os extremos de desempenho dos grupos avaliados.

Nos dois métodos, os três grupos com maiores erros estão associados ao almoço. Esse resultado pode estar relacionado à maior demanda e variabilidade dessa refeição, embora os dados disponíveis não permitam estabelecer uma relação causal.

Esses resultados possuem caráter preliminar e não determinam a seleção oficial dos modelos da Entrega 06.

### 8.7 Equidade

A análise identificou diferenças de desempenho entre cursos e tipos de refeição.

Entretanto, essas diferenças não são suficientes para caracterizar discriminação ou ausência de equidade, uma vez que os dados utilizados são sintéticos e os grupos apresentam diferentes níveis de demanda.

Variáveis como curso, turno e outras características contextuais, quando disponíveis, podem atuar como proxies de características socioeconômicas. Por esse motivo, sua utilização deve ser acompanhada de uma avaliação cuidadosa.

Não devem ser inferidos atributos sensíveis que não estejam presentes na base.

Em uma aplicação com dados reais, recomenda-se considerar:

- Quantidade de observações por grupo;
- Diferenças na escala da demanda;
- Cobertura e qualidade dos dados;
- Frequência de subestimações;
- Frequência de superestimações;
- Impactos operacionais dos erros.

O modelo deve auxiliar o planejamento das refeições, sem estabelecer critérios de elegibilidade ou restringir o acesso dos estudantes ao RU.

### 8.8 Subestimações e superestimações

Foram desenvolvidas funções para identificar três situações:

- Subestimação: previsão inferior ao valor observado;
- Superestimação: previsão superior ao valor observado;
- Acerto exato: previsão igual ao valor observado.

A subestimação pode contribuir para a produção insuficiente de refeições, enquanto a superestimação pode contribuir para o desperdício de alimentos.

Também foram desenvolvidas funções para identificar as observações com maiores erros absolutos e os casos mais críticos de subestimação e superestimação.

A execução definitiva dessas análises depende da disponibilização das previsões individuais dos modelos da Entrega 06.

O arquivo de métricas agregadas utilizado na análise preliminar não permite identificar datas específicas, calcular o viés ou determinar a frequência dos erros individuais.

### 8.9 Limitações da análise

Os resultados apresentados nesta seção foram obtidos a partir da base mock e das métricas dos baselines anteriores.

A análise definitiva deverá utilizar as previsões oficiais da Entrega 06, respeitando as partições temporais estabelecidas pela equipe.

As funções desenvolvidas estão preparadas para receber:

- Identificador da observação;
- Data;
- Tipo de refeição;
- Curso;
- Partição;
- Modelo;
- Valor observado;
- Valor previsto.

A análise por faixa de demanda deverá utilizar limites definidos a partir dos dados de treino.

Os resultados preliminares não substituem a avaliação oficial dos modelos.

## 9. Proposta de produto

### 9.1 Objetivo

Propõe-se o desenvolvimento de um painel de apoio ao planejamento diário da produção de refeições do Restaurante Universitário.

O objetivo é disponibilizar informações sobre a demanda prevista, permitindo que a equipe responsável pelo RU utilize essas estimativas como apoio à tomada de decisão.

### 9.2 Público-alvo

O produto é destinado principalmente aos profissionais responsáveis pelo planejamento, organização e produção das refeições do Restaurante Universitário.

### 9.3 Entradas do sistema

- Data da previsão;
- Tipo de refeição;
- Curso;
- Histórico de refeições servidas;
- Informações de calendário disponíveis antecipadamente;
- Informações sobre a cobertura dos dados.

A previsão deverá considerar somente informações disponíveis até o encerramento do dia anterior e informações conhecidas antecipadamente.

### 9.4 Saídas do sistema

- Quantidade prevista de refeições;
- Histórico da demanda;
- Comparação entre valores observados e previstos;
- Comparação da demanda por curso;
- Comparação por tipo de refeição;
- Indicadores históricos de erro;
- Alertas relacionados à cobertura dos dados.

A demanda total poderá ser apresentada quando houver cobertura adequada dos cursos.

### 9.5 Wireframe conceitual

```text
+------------------------------------------------------+
|              RU/UFPB - PREVISAO DE DEMANDA           |
+------------------------------------------------------+
| Data: [          ]                                   |
| Refeicao: [      ]        Curso: [               ]   |
+------------------------------------------------------+
| DEMANDA PREVISTA | HISTORICO | COBERTURA DOS DADOS    |
+------------------------------------------------------+
|                                                      |
|       GRAFICO DE DEMANDA OBSERVADA E PREVISTA         |
|                                                      |
+------------------------------------------------------+
| DEMANDA POR CURSO      | DEMANDA POR REFEICAO         |
+------------------------------------------------------+
| MAE       | RMSE       | ALERTAS E LIMITACOES         |
+------------------------------------------------------+
```

O painel apresentado corresponde a uma proposta conceitual de produto, não sendo realizada a implementação de um MVP nesta etapa.

As previsões devem funcionar como apoio à tomada de decisão, mantendo a responsabilidade final com a equipe gestora do RU.

## 10. Riscos e limitações

### 10.1 Principais riscos

| Risco | Possível impacto | Medida proposta |
|---|---|---|
| Dados sintéticos | Resultados diferentes da realidade do RU | Validar com dados reais |
| Cobertura incompleta | Previsões baseadas em informações insuficientes | Verificar a completude da extração |
| Degradação temporal | Redução da precisão ao longo do tempo | Monitorar os erros periodicamente |
| Subestimação | Produção insuficiente de refeições | Monitorar erros negativos e manter revisão humana |
| Superestimação | Desperdício de alimentos | Monitorar erros positivos e ajustar o planejamento |
| Uso inadequado das previsões | Decisões injustificadas sobre determinados grupos | Restringir o uso ao planejamento operacional |
| Capacidade desconhecida | Dificuldade de avaliar a viabilidade operacional | Incorporar informações reais de capacidade |
| Ausência de informações de custos | Impossibilidade de estimar impactos financeiros reais | Incorporar dados financeiros quando disponíveis |

### 10.2 Limitações dos dados simulados

A base mock permite desenvolver e testar a metodologia de análise, mas não representa necessariamente o comportamento real dos estudantes da UFPB.

Os resultados obtidos não devem ser interpretados como evidências definitivas sobre a demanda real ou sobre diferenças socioeconômicas entre os estudantes.

A utilização operacional do modelo dependerá da disponibilidade de dados reais, da qualidade das informações e da validação dos resultados.

### 10.3 Monitoramento

Após uma eventual implementação, recomenda-se acompanhar periodicamente:

- MAE e RMSE;
- Viés das previsões;
- Frequência de subestimações e superestimações;
- Desempenho por curso e refeição;
- Mudanças no comportamento da demanda;
- Cobertura dos dados.

O acompanhamento desses indicadores permitirá identificar possíveis perdas de desempenho e orientar futuras revisões do modelo.

### 10.4 Uso responsável

O sistema deve ser utilizado exclusivamente como ferramenta de apoio ao planejamento da produção de refeições.

As previsões não devem ser utilizadas para determinar quais estudantes podem acessar o Restaurante Universitário, restringir direitos ou substituir decisões administrativas sem avaliação humana.

## 11. Registro da contribuição individual

### Atividades realizadas

- [x] Desenvolvimento do notebook individual.
- [x] Implementação das funções de cálculo de erros.
- [x] Implementação das métricas MAE, RMSE e viés.
- [x] Implementação da análise por grupos.
- [x] Implementação da identificação de casos críticos.
- [x] Diagnóstico da qualidade da base mock.
- [x] Análise da demanda por curso e refeição.
- [x] Comparação preliminar dos erros dos baselines.
- [x] Consolidação das métricas por grupo.
- [x] Elaboração da proposta de produto.
- [x] Elaboração do wireframe.
- [x] Identificação dos riscos e limitações.
- [x] Verificação da disponibilidade das funções.
- [x] Elaboração do relatório individual.

### Pendências de integração

- [ ] Recebimento das previsões oficiais da Entrega 06.
- [ ] Execução da análise definitiva dos erros.
- [ ] Investigação dos casos individuais de subestimação e superestimação.
- [ ] Análise definitiva por período e faixa de demanda.
- [ ] Integração da contribuição ao notebook coletivo.

### Validação das funções

A verificação final confirmou a disponibilidade das seguintes funções no notebook:

| Função | Status |
|---|---|
| calcular_erros | OK |
| resumir_erros | OK |
| analisar_grupos | OK |
| identificar_casos_criticos | OK |
| preparar_previsoes | OK |
| comparar_equidade | OK |
| executar_analise | OK |
| visualizar_erros | OK |
| consolidar_metricas | OK |

A disponibilidade das funções não substitui a realização de testes completos com as previsões oficiais da Entrega 06.

## Considerações finais

A contribuição individual concentrou-se na análise de erros e equidade, na elaboração da proposta de produto e na identificação dos riscos e limitações do projeto.

Os resultados preliminares permitiram identificar diferenças de desempenho entre cursos e refeições, com destaque para o almoço, que apresentou os maiores erros nos baselines analisados.

As funções desenvolvidas estão preparadas para receber as previsões oficiais da equipe, permitindo a continuidade da análise durante a integração.

Não foram realizados treinamento de modelos, seleção do modelo vencedor, alterações na base compartilhada ou redefinição das partições oficiais nesta contribuição.