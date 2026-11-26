# Entrega 05: Maria Dionila

## Identificação

- Integrante: Maria Dionila
- Usuário GitHub: mariadionila
- Entrega: 05
- Branch: `entrega-05-mariadionila` (criada a partir de `develop/mock`)
- Parte da equipe: *Baselines, regressão e comparação*

## Atividades realizadas

- Reaproveitei os dois baselines da E04 (média do treino por curso×refeição e D-7), sem alterá-los.
- Implementei o primeiro modelo de regressão: **Ridge** em `Pipeline` + `ColumnTransformer`, com α escolhido por `GridSearchCV` apenas no treino, em 5 blocos temporais formados por datas inteiras (um mesmo dia nunca fica no treino e na validação da mesma rodada).
- Calculei a métrica principal (MAE por `dia × refeição × curso`) e as secundárias (RMSE, viés, MAE do total diário) para os três na mesma partição e nos mesmos casos.
- Montei o quadro obrigatório de comparação, interpretei o resultado e preparei três figuras para o relatório coletivo.
- Consultei o teste de 2026 (os resultados aparecem no notebook). Ele não foi usado para escolher hiperparâmetros nem para decidir entre o Ridge e outro modelo.

## Arquivos criados ou modificados

- `notebooks/individuais/entrega-05-mariadionila.ipynb`: notebook executável do início ao fim (base, partição, baselines, modelo, CV, quadro, resíduos, limites).
- `output/figuras/e05_residuos_validacao.png`, `e05_mae_dia_refeicao.png`, `e05_total_diario.png`: gráficos para o relatório.
- `requirements.txt`: adicionado `matplotlib==3.11.2` (necessário apenas para os gráficos; autorizado pela autora).
- `dados/processado/resultados_comparacao_e05.csv`: gerado pela execução (não versionado).

## Metodologia

- **Alvo e partição (congelados da E04):** quantidade servida em `D` por `data × refeição × curso`, prevista em `D-1`; treino 2019–2024 (33.822 linhas), validação 2025 (5.634), teste 2026 até 14/11 (4.914), só dias abertos.
- **Preditoras (todas conhecidas na véspera):** `lag_7`, `media_4sem` (D-7, D-14, D-21, D-28), `tendencia` (numéricas: imputação por mediana e padronização) e `dia_semana`, `mes`, `tipo_refeicao`, `curso` (categóricas: one-hot, `handle_unknown="ignore"`). Ficam fora quantidade/negadas de `D`, sobras, quantidade preparada, faltas e notas.
- **Estimação:** Ridge, α=100 (interior da grade 0,01–1000). Previsões negativas truncadas em zero. Atributos defasados calculados por data dentro de cada curso/refeição; transformações aprendidas só no treino.
- **Comparação honesta:** mesmos 5.634 casos (validação) e 4.914 (teste), todos com `D-7` disponível; mesmo tratamento para os três. Intervalo de confiança do ganho sobre o D-7 por bootstrap por dia (5.000 reamostras, semente 20261001).
- **Métrica:** MAE principal (unidade da decisão, trata falta e sobra com o mesmo peso porque `B`, `C` e `k` ainda não foram levantados); RMSE, viés (real − previsto) e MAE do total diário como secundárias. MAPE não é usado (demanda por curso perto de zero).

## Testes e verificações

Executei o notebook do início ao fim com `jupyter nbconvert --execute` no `.venv` (Python 3.12.10), sem erros. Verifiquei por `assert`: soma da base igual a 221.600 refeições servidas; grade completa de 51.750 linhas; datas de treino < validação < teste; em cada bloco da validação cruzada, nenhuma data nos dois lados e treino sempre anterior à validação; ausência de `NaN` nas três previsões nas linhas avaliadas. As métricas dos baselines na validação (MAE 2,67 e 2,14; total diário 42,91 e 15,04/15,05) coincidem com o relatório da E04.

## Resultados

Validação 2025 (5.634 linhas):

| Abordagem | MAE | RMSE | Viés | MAE total diário |
|---|---:|---:|---:|---:|
| Baseline trivial | 2,67 | 3,24 | +0,28 | 42,91 |
| Baseline operacional (D-7) | 2,14 | 2,95 | +0,01 | 15,05 |
| Modelo Ridge | **1,70** | **2,24** | +0,19 | **14,22** |

Teste 2026, consultado (4.914 linhas; não usado para escolher modelo): MAE 2,88 / 2,20 / **1,77**; RMSE 3,49 / 3,01 / **2,32**; viés +0,69 / +0,10 / +0,45; MAE total diário 48,29 / **13,84** / 15,38 (trivial / D-7 / modelo).

A validação cruzada temporal (blocos de datas inteiras, dentro do treino) serviu para escolher o α. O erro calculado nesses mesmos blocos não é apresentado como avaliação independente: **a comparação principal é a validação de 2025**. Os resultados de 2026 estão acima só como registro de que o teste foi consultado.

- O modelo supera os dois baselines **por linha** (MAE cerca de 20% menor que o D-7 na validação de 2025). O ganho sobre o D-7 na validação é de 0,44 refeição/linha, IC 95% [0,36; 0,52]; o modelo é melhor em 55,8% das linhas e pior em 41,1%.
- **No total diário o ganho não se sustenta:** na validação de 2025 o modelo é só 5% melhor que o D-7 (14,22 contra 15,05).
- O modelo tem viés positivo crescente (subestima: +0,19 por linha em 2025 ≈ 3 a 4 refeições/dia a menos, mais forte de agosto a dezembro), compatível com uma tendência linear que não acompanha o crescimento recente. Hipótese a confirmar; o D-7 tem viés quase nulo.
- Resíduos: |r| ≥ 8 em 0,28% das linhas (D-7: 2,41%); máximo +10,1 e mínimo −8,8. Viés mensal perto de zero de fevereiro a junho e positivo de agosto a dezembro. A análise completa de resíduos fica com Kaio Vitor; os números e gráficos estão no notebook (seção 8). As faixas diagonais no gráfico resíduo × previsto decorrem de o real ser inteiro.

## Limitações e pendências

- Dados sintéticos: nenhum número descreve o RU real; o gerador favorece padrões semanais e sazonais.
- `B`, `C` e `k` não levantados: o MAE não é custo econômico; se faltar refeição custar mais que sobrar, trocar por perda assimétrica.
- A regra D-7 é uma proposta da equipe, não a regra comprovada do RU.
- Hipóteses do Ridge (linearidade, variância constante) são fracas para contagens; os resíduos do almoço mostram heterocedasticidade.
- Depende de catraca fechada na véspera e de histórico por curso; curso novo não tem `lag_7`.
- Não usar para decidir subsídio ou elegibilidade.
- Pendente: conferir os números com o notebook coletivo e com o relatório consolidado por Letícia;

## Uso de IA generativa

Usei o Claude como apoio para estruturar o notebook, e redigir as interpretações e este relatório. Os baselines e a base por curso vêm do notebook coletivo da E04. Os números foram conferidos contra a execução.
