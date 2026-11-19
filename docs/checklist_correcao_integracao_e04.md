# Entrega 04 — fechamento e integração dos PRs

Preparado na branch local `codex/e04-consolidada`. Os PRs individuais #3, #4 e #5 foram mesclados em `develop/mock` e integrados nesta branch sem conflitos. O notebook `notebooks/E04_equipe02_dados_baseline.ipynb` é o único notebook coletivo para o professor. Os notebooks dos integrantes estão em `notebooks/individuais/` como histórico de contribuição.

## Concluído nesta consolidação

- [x] Alvo principal por `data × tipo_refeicao × curso`; total do RU derivado da soma dos cursos.
- [x] Dados brutos preservados, chaves e categorias críticas conferidas e saídas em `dados/processado/`.
- [x] Zero preenchido somente com cobertura completa do mock; modo real exige `cobertura_real.csv` e mantém quantidade vazia quando a extração é incompleta.
- [x] Valor do mock deixado vazio; campo monetário real pode ser mapeado somente depois de validar seu significado.
- [x] Partição temporal com treino 2019–2024, validação 2025 e teste 2026 reservado.
- [x] Pré-processador ajustado só no treino; categoria nova aceita na transformação.
- [x] Média e D-7 avaliados em 5.634 linhas abertas e completas; MAE global por curso/refeição 2,67 e 2,14, respectivamente.
- [x] Contrato, Canvas, memória da escuta, README, relatório de qualidade e PDF alinhados à unidade por curso.
- [x] Notebook executado do início ao fim pelo kernel Jupyter; as cinco células de código terminaram sem erro. O PDF final tem três páginas e foi conferido visualmente.
- [x] PRs individuais integrados em `codex/e04-consolidada` e notebooks movidos para `notebooks/individuais/`.

## Pessoas e publicação

- [ ] **Bianca:** confirmar o diagnóstico individual de vazamento, sua contribuição real e a declaração de IA, se aplicável. Seu PR #3 continua como registro individual.
- [ ] **Kaio:** confirmar diagnóstico, contribuição e quais blocos do PR #4 foram influenciados pelo Claude.
- [ ] **Dionila:** confirmar diagnóstico, contribuição e conferir que D-7 é uma regra proposta, não prática confirmada do RU. Seu PR #5 continua como registro individual.
- [ ] **Letícia:** conferir as contribuições, o notebook consolidado, o PDF e o quadro da equipe; confirmar a declaração de uso de Codex.
- [ ] **Publicação:** publicar `codex/e04-consolidada` por PR para `develop/mock`, obter as aprovações necessárias, mesclar e conferir os links do notebook e PDF acessíveis ao professor.
- [ ] **RU/SEBTT:** confirmar calendário, completude e horário das extrações, regra atual de planejamento, capacidade `k`, custos/preços, semântica do campo monetário e autorização de uso. Esses pontos não são inventados nesta E04 com mock.

## Regra simples para os PRs individuais

Preservar o trabalho dos três integrantes como histórico, mas manter **um só arquivo chamado `E04_equipe02_dados_baseline.ipynb` em `notebooks/`**. `entrega-04-lavine0524.ipynb` (Bianca), `entrega-04-kaiovitormr.ipynb` (Kaio) e `entrega-04-mariadionila.ipynb` (Dionila) estão em `notebooks/individuais/`. Os relatórios individuais permanecem em `docs/entregas/`. O README e o PDF apontam apenas para o coletivo como entrega.
