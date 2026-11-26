# Entrega 06 — Relatório preliminar do Pacote A2

**Equipe 02:** Letícia Braz, Bianca Lavine, Kaio Vitor e Maria Dionila  
**Escopo:** dados inteiramente sintéticos; uso somente metodológico.

## 1. Resumo executivo

Foram comparados, nas mesmas 5.634 observações de 2025, o baseline D-7, Ridge, árvore de decisão e Random Forest. O Ridge obteve o menor MAE (1,703) e foi selecionado provisoriamente. A decisão ainda não é operacional: calendário, cobertura, capacidade e custos reais não foram fornecidos.

## 2. Decisão e contexto

A previsão estima, em D-1, refeições servidas em D por data, refeição e curso. O produto apoia o planejamento de produção. Não pode restringir acesso ao RU nem substituir a decisão da equipe gestora.

## 3. Formulação

Trata-se de regressão. O alvo é a contagem de eventos `servida`. A métrica principal é MAE; RMSE e viés são secundárias. A perda é simétrica somente porque custos de falta e sobra não foram levantados.

## 4. Dados

A base mock tem 221.600 refeições servidas. O grão é `data × tipo_refeicao × curso`. Treino: 2019–2024, 33.822 linhas; validação: 2025, 5.634; teste identificado em 2026, 4.914, mas não usado na E06. Zeros só são criados em combinações com cobertura conhecida.

## 5. Método e validação

O pipeline parte dos CSVs brutos, monta a grade coberta e calcula D-7, média de quatro semanas, tendência, dia da semana, mês, refeição e curso. `ColumnTransformer` faz imputação, escala e codificação dentro de cada ajuste. Cinco dobras expansivas de datas inteiras escolhem hiperparâmetros apenas no treino.

| Candidato | Grade testada | Melhor configuração |
|---|---|---|
| Ridge | alfa 10, 100, 1000 | alfa 100 |
| Árvore | profundidade 4/8; folha 5/20 | profundidade 4; folha 5 |
| Random Forest | profundidade 8/sem limite; folha 2/10 | profundidade 8; folha 10; 100 árvores |

## 6. Resultados

| Abordagem | MAE | RMSE | Viés real−previsto | Busca (s) | Ajuste final (s) |
|---|---:|---:|---:|---:|---:|
| Ridge | **1,703** | **2,238** | 0,194 | 0,895 | 0,116 |
| Random Forest | 1,859 | 2,604 | 0,725 | 228,732 | 5,106 |
| Árvore | 1,883 | 2,488 | 0,212 | 1,499 | 0,137 |
| D-7 proposto | 2,139 | 2,951 | 0,007 | 0 | 0 |
| Média do treino | 2,667 | 3,238 | 0,279 | 0 | 0 |

Os tempos são da execução de referência e variam por computador. O Ridge é mais preciso e muito mais barato que a floresta neste mock. O teste de 2026 não foi usado ou reavaliado na E06.

## 7. Operação, limiar e capacidade

Não existe limiar de classificação. A saída provisória é `max(0, arredondar(previsão))`. Não foi aplicado teto porque a capacidade `k` é desconhecida. Quando informada, o produto deve exibir previsão, recomendação limitada e alerta de excesso separadamente.

## 8. Erros e equidade operacional

O Ridge tem maior MAE no almoço (2,254) e nos cursos D (1,879), B (1,858) e F (1,828). Os dez piores casos têm erro absoluto entre 8,39 e 10,13 refeições. Há subestimações concentradas em alguns meses do segundo semestre. Curso e refeição são grupos operacionais; com dados sintéticos, as diferenças não comprovam discriminação. Não se devem inferir atributos sensíveis ausentes.

## 9. Produto preliminar

O painel deve mostrar data, refeição, cobertura, total previsto, previsão por curso, histórico, faixa de erro e alertas. A cobertura incompleta deve impedir a apresentação silenciosa do total. Toda recomendação exige revisão humana.

## 10. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Dados sintéticos | desempenho não representa o RU | validar com dados reais |
| Calendário/cobertura errados | zeros ou previsões falsos | contrato e alerta de completude |
| Mudança temporal | degradação | monitorar MAE, RMSE e viés |
| Subestimação/sobra | falta ou desperdício | levantar custos e revisar perda |
| Capacidade desconhecida | recomendação inviável | incorporar `k` confirmado |
| Uso indevido | restrição injusta | limitar ao planejamento e manter revisão humana |

## 11. Feedback do demandante

Ainda não há validação institucional sobre regra atual, custos, capacidade, calendário real ou disponibilidade das fontes em D-1. Esses itens precisam ser confirmados antes de implantação.

## 12. Reprodutibilidade, contribuições e IA

Execute `notebooks/E06_equipe02_relatorio_preliminar.ipynb` do início ao fim. As versões estão em `requirements.txt`; a semente é 2026. O notebook salva comparação e previsões em `dados/processado/`.

- Bianca Lavine: entrega completa da responsabilidade atribuída — base, validação temporal, D-7 e Ridge.
- Kaio Vitor: entrega parcial — funções, análise preliminar, produto, wireframe e riscos foram entregues; a análise definitiva dependia das previsões oficiais e foi executada na consolidação.
- Maria Dionila: não entregou PR individual da E06 até esta consolidação. O trabalho da E05 foi reaproveitado como referência, sem ser contado como E06.
- Letícia Braz: implementou árvore, Random Forest, comparação comum, correções e consolidação.

Bianca declarou uso de Codex; Kaio deve manter a declaração de IA correspondente ao apoio usado; Codex auxiliou a coordenação na integração e revisão. A equipe deve conferir e explicar o conteúdo.
