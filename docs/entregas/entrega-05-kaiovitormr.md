# Entrega 05: Kaio Vitor

## Identificação

- Integrante: Kaio Vitor
- Usuário GitHub: kaiovitormr
- Entrega: 05
- Branch: `entrega-05-kaiovitormr`

## Atividades realizadas

Fiquei com vazamento, validação e resíduos. Revisei se as variáveis do modelo respeitam o que se sabe na véspera, confirmei a partição por data, conferi se os baselines usam a mesma partição e a mesma métrica e analisei os resíduos dos baselines. A análise do modelo de regressão entra quando ele estiver no notebook coletivo `[pendente]`.

## Arquivos criados ou modificados

- `notebooks/individuais/entrega-05-kaiovitormr.ipynb`: análise de vazamento, partição e resíduos. Ele roda o notebook coletivo por baixo e não altera esse arquivo.
- `docs/entregas/entrega-05-kaiovitormr.md`: este relatório.

## Metodologia

- Base: `notebooks/E04_equipe02_dados_baseline.ipynb`, executado no `.venv` do projeto.
- Vazamento: comparei as colunas de entrada com a classificação da Entrega 4.
- Partição: por data, sem sorteio, mantida como na Entrega 4 por decisão da Letícia, já que os dados são um mock.
- Resíduo = quantidade servida real menos a previsão, na validação.

## Testes e verificações

**Vazamento**
- As entradas do modelo são `dia_semana`, `mes`, `tipo_refeicao` e `curso`. Todas são conhecidas na véspera.
- O alvo (`quantidade_servida`) não está nas entradas.
- `aberto` vem do calendário (segunda a sábado) e não usa os eventos do dia previsto. `aberto` e `extracao_completa` são `True` em todo o treino e não entram no modelo.
- As 7.380 linhas fora do modelo são os 410 domingos vezes 18 combinações de curso e refeição.
- `cadastro_cursos` usa a base inteira, mas só serve para conferir os cursos e não alimenta a previsão.
- `valor_observado` (R$) está vazio no mock. O alvo é `quantidade_servida`.

**Partição**
- Treino 33.822 linhas, validação 5.634 e teste 4.914, com cortes em 31/12/2024 e 31/12/2025. Ordem das datas conferida.

**Mesma partição e métrica**
- Os dois baselines usam as mesmas 5.634 linhas da validação, com MAE e RMSE. Nenhuma linha ficou sem previsão do D-7.
- `[pendente: confirmar que o modelo usa as mesmas 5.634 linhas e as mesmas métricas]`

## Resultados

| Abordagem | MAE | RMSE |
|---|---:|---:|
| Média do treino | 2,67 | 3,24 |
| D-7 (mesma refeição, 7 dias antes) | 2,14 | 2,95 |
| Modelo | `[pendente]` | `[pendente]` |

**Resíduos dos baselines (validação)**
- O D-7 tem resíduo médio de 0,01 e desvio de 2,95. A média do treino tem 0,28 e 3,23. O D-7 erra menos, mas tem caudas maiores (de -15 a +15).
- Na volta às aulas (semanas de 09/02 e 10/08) o D-7 subestima em cerca de 4 refeições, porque olha a semana anterior, que era recesso. Na primeira semana do recesso (06/07 e 28/12) superestima, pelo motivo contrário.
- A média do treino subestima de forma constante de agosto a dezembro de 2025, o que indica mudança de nível da demanda.
- O almoço tem o maior erro (desvio de 3,55 no D-7). Nenhum curso destoa.
- A mudança de nível coincide com o número de vínculos ativos, que é de 117 até 2025.1, 138 em 2025.2 e 144 em 2026.
- `[pendente: resíduos do modelo]`

## Limitações e pendências

- Os dados são sintéticos. Nenhum número aqui descreve o RU real.
- O erro típico é de cerca de 3 refeições por curso, por refeição e por dia, o que é alto perto de uma média de 5.
- O recesso do mock é fixo (janeiro e julho inteiros), então os erros dessas semanas refletem a regra do gerador.
- Parte do crescimento da demanda (o teste tem média 14,2% acima do treino) coincide o aumento de vínculos ativos.
- O modelo atual não vê o início e o fim do período letivo nem o número de vínculos ativos. As duas informações são conhecidas na véspera e poderiam entrar.
- Com dados reais, `aberto` e a lista de cursos dependerão do calendário e do cadastro do RU e precisam ser reconferidos.
- Não há semente aleatória fixada no notebook coletivo, o que passa a importar quando o modelo entrar.
- Pendente: resíduos do modelo da Dionila.

## Uso de IA generativa

Usei o Claude como apoio durante toda a entrega: para tirar dúvidas, sugerir e ajudar a rodar o código das células do notebook (vazamento, partição e resíduos), orientar o uso do Git e rascunhar este relatório. Como a ajuda passou por todas as partes, não separei trechos específicos.