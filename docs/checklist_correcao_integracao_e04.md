# Entrega 04 — fechamento e integração dos PRs

Preparado na branch local `codex/e04-consolidada`. Os PRs individuais #3, #4 e #5 **não foram alterados nem integrados**. Os três PRs continuam abertos e adicionam arquivos diferentes; nenhum substitui o notebook coletivo. O notebook `notebooks/E04_equipe02_dados_baseline.ipynb` é o único notebook coletivo para o professor. Os notebooks dos integrantes serão guardados em `notebooks/individuais/` como histórico de contribuição.

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

## Pessoas e publicação

- [ ] **Bianca:** confirmar o diagnóstico individual de vazamento, sua contribuição real e a declaração de IA, se aplicável. Seu PR #3 continua como registro individual.
- [ ] **Kaio:** confirmar diagnóstico, contribuição e quais blocos do PR #4 foram influenciados pelo Claude.
- [ ] **Dionila:** confirmar diagnóstico, contribuição e conferir que D-7 é uma regra proposta, não prática confirmada do RU. Seu PR #5 continua como registro individual.
- [ ] **Letícia:** conferir as contribuições, o notebook consolidado, o PDF e o quadro da equipe; confirmar a declaração de uso de Codex.
- [ ] **Integração:** aprovar e mesclar os PRs #3, #4 e #5 em `develop/mock` como contribuições individuais, seguindo as aprovações exigidas pelo GitHub. Depois, atualizar a branch consolidada com `develop/mock`, mover os três notebooks para `notebooks/individuais/`, executar o notebook final e publicar esta branch por PR. Conferir links acessíveis ao professor.
- [ ] **RU/SEBTT:** confirmar calendário, completude e horário das extrações, regra atual de planejamento, capacidade `k`, custos/preços, semântica do campo monetário e autorização de uso. Esses pontos não são inventados nesta E04 com mock.

## Regra simples para os PRs individuais

Preservar o trabalho dos três integrantes como histórico, mas manter **um só arquivo chamado `E04_equipe02_dados_baseline.ipynb` em `notebooks/`**. Os PRs atuais criam `E04_ru_ufpb.ipynb` (Bianca), `entrega-04-kaiovitormr.ipynb` (Kaio) e `entrega-04-mariadionila.ipynb` (Dionila), todos com nomes diferentes do coletivo. Após mesclá-los, mover esses três arquivos para `notebooks/individuais/` no PR final. Os relatórios individuais podem permanecer em `docs/entregas/`. O README e o PDF devem apontar apenas para o coletivo como entrega.
