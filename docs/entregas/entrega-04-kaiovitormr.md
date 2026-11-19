# Entrega 04: Kaio Vitor

## Identificação

- Integrante: Kaio Vitor
- Usuário GitHub: kaiovitormr
- Entrega: 04
- Branch: `entrega-04-kaiovitormr`

## Atividades realizadas

Conferi os três CSVs do mock sem alterar os brutos, montei a base diária de referência (só refeições servidas), propus a divisão temporal em treino, validação e teste e classifiquei as variáveis quanto a vazamento.

## Arquivos criados ou modificados

- `notebooks/entrega-04-kaiovitormr.ipynb`: auditoria, base diária, partição e classificação de variáveis. Cada conferência entra numa tabela final.
- `docs/entregas/entrega-04-kaiovitormr.md`: este relatório.

## Metodologia

- Leitura dos CSVs como texto (`dtype=str`), com os vazios preservados. Nenhum arquivo bruto foi alterado.
- Conferências de contagens, vazios, chaves, categorias, formatos, ligações entre arquivos, componentes e calendário. Cada uma sai como `ok`, `ATENÇÃO` (valor diferente do esperado) ou `achado` (observação sem valor esperado).
- Fase do calendário de cada evento: início do recesso mais recente anterior à data.
- Base diária só com refeições servidas. Domingo fica fora, sem preencher com zero.
- Partição por data, sem sorteio, com cortes em 31/12/2024 e 31/12/2025.
- Vazamento classificado em permitida, proibida por tempo e proibida por consequência da decisão, com corte no fim do dia anterior (D-1).

## Testes e verificações

Rodei o notebook do início ao fim no ambiente `.venv` do projeto (Python 3.12.0), com o kernel reiniciado antes. Resultado: 71 conferências, 71 `ok`, 0 `ATENÇÃO` e 15 `achado`. Não testei com dados reais.

## Resultados

- As contagens batem com o relatório do mock: 224.880 eventos (221.600 servidas e 3.280 negadas), 2.016 vínculos e 5.922 inscrições.
- Base diária de 2.465 dias. Os 410 dias sem evento são todos domingos.
- Partição:

| Conjunto | Intervalo | Dias | Servidas por dia |
|---|---|---:|---:|
| Treino | 01/01/2019 a 31/12/2024 | 1.879 | 87,9 |
| Validação | 01/01/2025 a 31/12/2025 | 313 | 92,9 |
| Teste | 01/01/2026 a 14/11/2026 | 273 | 100,4 |

- A média do teste é 14,2% maior que a do treino. A demanda cresce com o tempo, e quem faz os baselines precisa saber disso.
- `tipo_acesso` repete `tipo_auxilio` em todos os eventos, então as duas não devem entrar juntas.
- A seção 8 do notebook classifica 12 variáveis. Três exemplos:
  - Permitida: dia da semana, ou refeições servidas até D-1.
  - Proibida por tempo: `frequencia_percentual`, que só é consolidada no fim do período.
  - Proibida por consequência da decisão: quantidade preparada de refeições. Não existe no mock, mas é a decisão que a previsão deve orientar.

## Limitações e pendências

- Os dados são sintéticos e os cortes da partição são provisórios.
- Assumi que a previsão é feita no fim de D-1. O grupo precisa confirmar.
- O dicionário diz que o mock não gera cancelamentos, mas existem vínculos `cancelado`. Falta perguntar à Letícia.
- Há 3 vínculos que saem de `ativo` e voltam. Ainda não confirmei quais são.
- A integração no notebook único é com a Letícia. O pré-processamento e os baselines são de outras integrantes.

## Uso de IA generativa

Usei o Claude (Anthropic) para otimizar a entrega e sugerir código. Os resultados foram conferidos rodando o notebook, e consigo explicar cada parte.
Trechos influenciados: [preencher: quais seções do notebook e do relatório].