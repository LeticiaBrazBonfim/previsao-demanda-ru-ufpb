# Entrega 05 — Pacote A1: baselines e primeiro modelo

**Equipe 02:** Letícia Braz, Bianca Lavine, Kaio Vitor e Maria Dionila  
**Escopo:** dados inteiramente sintéticos. Nenhum resultado descreve o RU real.

## 1. Decisão e formulação

O projeto prevê, na véspera, a quantidade servida em cada combinação de data, refeição e curso. A previsão apoia o planejamento da produção; não decide acesso ou subsídio. O total do RU é derivado da soma dos cursos somente com cobertura completa.

## 2. Dados, contrato e auditoria

O alvo conta identificadores únicos com evento `servida`. Eventos negados são excluídos. No mock, segunda a sábado são dias abertos e a extração é completa; por isso, ausência de evento em combinação coberta vira zero. Nos dados reais, calendário, cursos ativos e completude da extração deverão ser informados e auditados.

Treino cobre 2019–2024 (33.822 linhas), validação cobre 2025 (5.634) e teste cobre 2026 até 14/11 (4.914). A validação cruzada usa cinco blocos cronológicos de datas inteiras dentro do treino. Nenhuma transformação é aprendida na validação.

## 3. Baselines e modelo

- Baseline trivial: média do treino por curso e refeição.
- Baseline operacional proposto: quantidade da mesma combinação sete dias antes (D-7). A regra real do RU ainda não foi confirmada.
- Primeiro modelo: Ridge com `ColumnTransformer` e `Pipeline`. Entradas: D-7, média de quatro semanas, tendência, dia da semana, mês, refeição e curso. Imputação, escala e codificação são ajustadas apenas no treino. O alfa 100 foi escolhido por validação cruzada temporal.

## 4. Avaliação e comparação obrigatória

MAE por linha é a métrica principal, pois mede refeições na unidade da decisão. RMSE, viés e MAE do total diário são secundárias. Como custos de falta, sobra e capacidade ainda não foram levantados, falta e sobra recebem peso igual.

| Abordagem | Hiperparâmetro | MAE | RMSE | Viés real−previsto | MAE total diário |
|---|---:|---:|---:|---:|---:|
| Média do treino | — | 2,667 | 3,238 | 0,279 | 42,907 |
| D-7 proposto | — | 2,139 | 2,951 | 0,007 | 15,045 |
| Ridge | alfa 100 | **1,703** | **2,238** | 0,194 | **14,217** |

Todos os métodos foram avaliados nas mesmas 5.634 linhas de 2025. O Ridge reduz o MAE em aproximadamente 20% contra D-7. O ganho no total diário é menor, cerca de 5%, e o viés positivo indica leve subestimação.

## 5. Resíduos, limites e casos problemáticos

O almoço apresenta maior erro. O Ridge tende a subestimar entre agosto e dezembro; os maiores resíduos absolutos ficam em torno de 9–10 refeições por combinação de curso e refeição. Mudanças de nível, recessos e cursos sem histórico podem degradar o desempenho. O mock favorece padrões semanais e não comprova generalização para dados reais.

O teste de 2026 foi consultado no notebook individual da regressão e não foi usado para escolher o alfa. Mesmo assim, deixou de ser um teste totalmente intocado; por isso, a E06 não o reutiliza para seleção ou comparação.

## 6. Reprodução e contribuições

Execute `notebooks/E05_equipe02_pacote_a1.ipynb` do início ao fim com as versões de `requirements.txt`. O notebook refaz a base, ajusta o pipeline, salva os gráficos e apresenta as observações extremas.

Maria Dionila fez a entrega completa de baselines, Ridge, validação e resíduos. Bianca Lavine fez entrega parcial para a consolidação: executou o Random Forest, mas o colocou dentro do notebook final da E04 e não selecionou hiperparâmetros; o registro individual foi preservado e a E04 restaurada. Kaio Vitor fez entrega parcial: concluiu vazamento, partição e resíduos dos baselines, mas deixou pendente a parte dependente do modelo, completada no coletivo. Letícia Braz coordenou, corrigiu, separou e consolidou as entregas. Maria e Kaio declararam uso de Claude; Bianca declarou uso de Codex; Codex também apoiou a consolidação. A equipe deve conferir e explicar o conteúdo.
