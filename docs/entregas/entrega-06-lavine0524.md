# Contribuição Individual — Entrega 06

## Identificação

- **Integrante:** Bianca Lavine
- **Usuário GitHub:** `lavine0524`
- **Branch:** `entrega-06-lavine0524`
- **Responsabilidade:** base comum, validação temporal, baseline e modelo linear.

## Seção 4 — Dados

A execução usa os CSVs sintéticos do mock em `dados/bruto/mock/`. A catraca tem 224.880 registros: foram mantidos os 221.600 eventos com `situacao_evento = servida`; os 3.280 eventos negados não compõem o alvo. O identificador `id_registro_utilizacao` foi verificado como único.

O grão da modelagem é uma linha por `data + tipo_refeicao + curso`. O alvo é `quantidade_servida`, contado por identificadores de eventos servidos. A chave identificadora da observação é formada por data, tipo de refeição e curso. No mock, a cobertura é completa no intervalo simulado; por isso, combinações sem eventos recebem zero. `aberto` (calendário simulado) e `extracao_completa` servem para selecionar linhas elegíveis, não são preditoras. O total do RU é derivado da soma dos cursos e só deve ser considerado quando todos os cursos da data/refeição estão cobertos.

As variáveis disponíveis na véspera e usadas como entradas são dia da semana, mês, tipo de refeição e curso. `quantidade_servida` é o alvo; a quantidade do próprio dia não entra nas entradas do Ridge. `cadastro_cursos` não é usado como preditora. Os cortes comuns preservados da E4/E5 são: treino até 31/12/2024 (33.822 linhas), validação em 2025 (5.634 linhas) e teste a partir de 01/01/2026 (4.914 linhas). Todas as combinações de refeição/curso de uma mesma data permanecem na mesma partição.

## Seção 12 — Reprodutibilidade

O notebook `notebooks/individuais/entrega-06-lavine0524.ipynb` refaz a base a partir dos CSVs e registra as saídas executadas. O pré-processamento está dentro de um `Pipeline`: imputação pela mediana e padronização para variáveis numéricas; imputação pela moda e `OneHotEncoder(handle_unknown="ignore")` para tipo de refeição e curso.

A validação cruzada usa cinco dobras cronológicas construídas a partir das datas únicas do treino (`TimeSeriesSplit`). Em cada dobra, todas as linhas de uma data permanecem juntas e o Pipeline é ajustado novamente apenas nas datas daquele treino da dobra. A grade testada foi `alpha = 0.1, 1, 10, 100`; o parâmetro foi escolhido pelo menor MAE médio nas dobras de treino. O alpha selecionado foi 0,1 (MAE médio 2,2638; RMSE médio 2,8480). O Ridge final foi ajustado no treino completo e avaliado na validação de 2025: MAE 2,439 e RMSE 3,038 em 5.634 observações.

O baseline operacional recalculado para a mesma validação foi D-7: repetir a quantidade da mesma combinação curso/refeição observada sete dias antes. Como a regra atualmente usada pelo RU não foi confirmada, D-7 é descrito somente como heurística proposta. Na validação, teve MAE 2,139 e RMSE 2,951 em 5.634 observações comparáveis. A escolha do modelo final da equipe cabe à consolidação coletiva; estes resultados não usam o teste.

A busca levou aproximadamente 0,49 s e o ajuste final do Ridge, 0,02 s nesta execução; os tempos variam conforme o computador. Ridge é determinístico e não requer semente aleatória. As versões usadas foram numpy 2.5.4, pandas 3.1.0 e scikit-learn 1.9.1, fixadas em `requirements.txt`. O teste de 2026 permaneceu reservado: não foi usado para ajustar o pré-processador, escolher alpha ou calcular as métricas relatadas.

## Arquivos da contribuição

- `notebooks/individuais/entrega-06-lavine0524.ipynb`: notebook individual para consolidação posterior pela responsável pelo notebook coletivo.
- `dados/saidas/e06_bianca/previsoes_validacao_bianca.csv`: previsões por observação, com ID, data, refeição, curso, partição, modelo, valor observado e previsto, e parâmetros.
- `dados/saidas/e06_bianca/previsoes_total_ru_validacao_bianca.csv`: previsões totais derivadas dos cursos com cobertura completa.
- `dados/saidas/e06_bianca/validacao_cruzada_ridge_por_dobra.csv` e `resumo_validacao_cruzada_ridge.csv`: métricas e tempos por dobra/alpha e médias usadas na seleção.
- `dados/saidas/e06_bianca/registro_execucao_e06_bianca.csv`: parâmetro selecionado, perda, métricas e tempos.

**Uso de IA:** Codex auxiliou na implementação, execução e conferência do bloco. A autora deve revisar e conseguir explicar o código e os resultados antes da consolidação.
