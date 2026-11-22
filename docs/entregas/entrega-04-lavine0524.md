# Entrega 04: Bianca Lavine

## Identificação

- **Integrante:** Bianca Lavine
- **Usuário GitHub:** `lavine0524`
- **Entrega:** 04 — Base analítica, pré-processamento e baseline
- **Branch:** `entrega-04-lavine0524`
- **Repositório:** [previsao-demanda-ru-ufpb](https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb)

## Atividades realizadas

Li e auditei os arquivos do mock — `catraca_ru.csv`, `estudantes.csv` e `matriculas_componentes.csv` — e construí uma base diária com a quantidade de refeições servidas por data e tipo de refeição.

Também verifiquei a associação temporal dos eventos aos períodos letivos e completei a grade diária, preenchendo com zero as combinações de data e refeição sem eventos.

## Arquivos criados ou modificados

- `notebooks/individuais/entrega-04-lavine0524.ipynb`: notebook de exploração e auditoria.
- `docs/entregas/entrega-04-lavine0524.md`: este relatório.
- `dados/processado/base_analitica_diaria.csv`: base diária processada.

## Metodologia

- **Filtro dos eventos:** mantive os registros com `situacao_evento == "servida"`.
- **Preservação da contagem:** verifiquei a unicidade de `id_registro_utilizacao` para evitar contar o mesmo evento mais de uma vez.
- **Associação temporal:** comparei a data da refeição com o início e o fim do período letivo registrado para o estudante.
- **Grade diária:** agrupei os eventos por data e tipo de refeição e completei as combinações ausentes com zero.

## Verificações e resultados

- A catraca tinha **224.880 registros**: **221.600** refeições servidas e **3.280** eventos negados.
- Não foram encontrados identificadores de evento duplicados.
- **205.823 eventos** tiveram período letivo compatível; **15.777** não tiveram período único compatível.
- Os eventos sem período compatível se concentraram em janeiro, julho e dezembro. A relação desses eventos com recessos ainda precisa ser confirmada.
- A base diária completa contém **8.625 linhas**: **2.875 datas × 3 tipos de refeição**.
- A soma da base completa permaneceu em **221.600 refeições servidas**.

## Limitações e pendências

Os dados utilizados são sintéticos e pertencem ao mock. Ainda é necessário confirmar, usando o calendário ou as regras de geração dos dados, se os eventos sem período letivo compatível correspondem a refeições durante recessos.