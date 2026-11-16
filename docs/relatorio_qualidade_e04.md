# Entrega 04 — relatório de qualidade e baseline

**Equipe 02:** Letícia Braz, Bianca Lavine, Kaio Vitor e Maria Dionila

**Repositório:** https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb

**Notebook coletivo:** `notebooks/E04_equipe02_dados_baseline.ipynb`

**Natureza:** piloto com dados inteiramente sintéticos, preparado em 15/11/2026. Nenhum resultado numérico deste relatório descreve o RU real da UFPB.

## 1. Contrato e decisão

Na véspera (`D-1`), estimamos a quantidade de refeições que serão **servidas** em `D`, por `data × tipo_refeicao × curso`. O alvo conta IDs distintos de eventos de catraca com `situacao_evento = servida`. O total do RU é uma soma secundária dos cursos. A população simulada contém seis cursos técnicos fictícios, três refeições, uma unidade e datas de 01/01/2019 a 14/11/2026. Os três CSVs brutos foram gerados com a semente `20261001` e permanecem preservados. A atualização diária e o horário de disponibilidade são hipóteses do piloto, não fatos confirmados pelo RU.

O projeto da Entrega 3 pede quantidade e valor por curso. Esta E04 entrega a **quantidade** e deixa `valor_observado` vazio porque o mock não possui valor. A referência aproximada de R$ 16 por refeição não é preço confirmado nem custo observado. Se a extração real contiver valor por evento servido, a equipe deverá validar a unidade, a semântica e a vigência antes de somá-lo na mesma chave. Isso ainda não permitiria inferir economia ou elegibilidade a subsídio.

## 2. Qualidade: problema, decisão e efeito

| Base ou problema | Decisão aplicada | Evidência e efeito |
|---|---|---|
| Catraca: 224.880 tentativas. | Contar somente `servida`; `negada` não é refeição consumida. | 221.600 servidas e 3.280 negadas; a soma da base por curso e da base total reconcilia as 221.600 servidas. |
| Chaves, datas e categorias críticas. | Conferir IDs únicos, vínculo, data, refeição, curso e situação antes de agregar. Confrontar curso da catraca com o cadastro por vínculo. | 0 IDs de evento duplicados, 0 datas inválidas, 0 eventos sem vínculo cadastrado, 0 chaves duplicadas de estudante/período ou componente e 0 situações inesperadas no mock. O confronto preservou 224.880 linhas e encontrou 0 cursos divergentes. |
| Ausências nos três CSVs. | Mostrar a taxa por coluna com denominador; não eliminar linhas automaticamente. | 0 valores ausentes nos 224.880 eventos, 2.016 vínculos/períodos e 5.922 componentes atuais. A ausência em fonte real precisará de interpretação por campo, tempo e grupo. |
| Componentes podem ter várias linhas por vínculo/período. | Conferir a chave estrangeira composta; não juntar componentes aos eventos porque nenhum atributo acadêmico entra no baseline. | 0 chaves de componente sem estudante/período. Não há multiplicação de refeições por uma junção desnecessária. |
| Dia, refeição e curso sem evento. | Usar a cobertura completa **conhecida do gerador**. Preencher zero somente onde a extração é completa. | 2.875 datas × 3 refeições × 6 cursos = 51.750 linhas. Há 11.990 zeros: 7.380 em domingos fechados e 4.610 em dias abertos. A soma permanece 221.600. |
| Ausência de cobertura real. | Exigir `cobertura_real.csv` com data, refeição, curso ativo, abertura e completude. Marcar quantidade vazia se a extração for incompleta. | O notebook não roda no modo real sem essa evidência. Linhas incompletas não entram no treino nem nas métricas, e totais com algum curso incompleto ficam vazios. |
| Valores extremos no mock. | Mostrar distribuição por refeição em dias abertos; não remover extremos sem investigar. | Máximos por curso/dia: 19 almoços, 14 cafés e 14 jantares. Médias: 7,45, 3,97 e 3,57 refeições, respectivamente, nos dias abertos. |

As datas exatas, categorias fixas e calendário semanal são testes **do mock**, separados das verificações gerais. Em fonte real, o esquema, as categorias e os cortes temporais deverão ser mapeados antes de executar. Não se deve concluir que um dia sem registro significa RU fechado ou consumo zero.

## 3. Partição e prevenção de vazamento

O cenário é fazer uma previsão a cada véspera, com histórico atualizado. O treino cobre 2019–2024 (**33.822** linhas em dias abertos), a validação cobre 2025 (**5.634** linhas, 313 dias abertos) e o teste reservado cobre 2026 até 14/11 (**4.914** linhas). Datas não se sobrepõem. A Entrega 3 citava 2025 como histórico e 2026 para teste; os anos anteriores do mock permitem uma validação adicional em 2025, mantendo 2026 intocado para avaliação final.

As entradas são `dia_semana`, `mes` (numéricas), `tipo_refeicao` e `curso` (categóricas). O `Pipeline` com `ColumnTransformer` usa mediana e escala nas numéricas, moda e `OneHotEncoder(handle_unknown="ignore")` nas categóricas. O `fit` ocorre somente no treino; validação e teste recebem `transform`. Os três conjuntos possuem o mesmo número de atributos transformados. Um curso novo é aceito pelo codificador, mas média por curso e D-7 ainda exigem histórico: o notebook mostra quantas linhas ficam sem comparação, sem inventar previsão. Como o mock não tem faltantes nessas entradas, a imputação é uma precaução estrutural; calendário, curso ou chave ausente não são imputados. Mediana e moda pressupõem poucas ausências, e muitas faltas seriam sinal de falha da fonte. A escala apenas compara magnitudes, sem provar uma relação linear de mês ou dia da semana com consumo; erros concentrados em feriados, meses ou cursos pedem revisão dessas hipóteses.

Não entram como preditoras: quantidade e valor de `D`, eventos de catraca de `D`, faltas e notas finais do semestre, refeições preparadas e sobras. `D-7` só é admissível se a catraca estiver completa antes da previsão. A média é calculada exclusivamente no treino. O teste de 2026 não foi usado para escolher a regra.

## 4. Baselines e métricas de validação

O baseline trivial é a média de 2019–2024 por curso e refeição. O segundo repete a quantidade do mesmo curso/refeição **exatamente sete dias antes**. É uma heurística proposta pela equipe; não foi comprovada como regra atual do RU. Em 2025, o D-7 pode usar observações anteriores de 2025 apenas porque o cenário simula previsões sucessivas, feitas dia após dia.

MAE em refeições por curso/refeição é a métrica principal, pois expressa o erro médio na unidade da decisão. RMSE complementa a leitura de erros grandes. Sem capacidade `k` e custos `B/C` confirmados, essas métricas não são custo econômico ótimo. A comparação usa os mesmos **5.634** casos para as duas regras, todos em dias abertos e com cobertura completa.

| Validação de 2025 | MAE média | MAE D-7 | RMSE média | RMSE D-7 |
|---|---:|---:|---:|---:|
| Por `data × refeição × curso` (5.634 linhas) | 2,67 | 2,14 | 3,24 | 2,95 |
| Total diário do RU (313 dias completos) | 42,91 | 15,04 | 45,10 | 27,19 |

Os erros detalhados de cada curso e refeição são gerados no CSV `resultados_baselines_validacao_por_curso.csv` e aparecem no notebook. D-7 melhora o MAE global do mock, mas **não vence a média em todas as combinações**; por exemplo, no café do curso B e no jantar dos cursos B, D e F. O padrão semanal implantado pelo gerador favorece D-7 e não prova superioridade nos dados reais. Os 410 domingos fechados não entram nas métricas.

## 5. Diagnóstico individual de vazamento — validar pessoalmente

Os exemplos abaixo foram preparados na consolidação. **Cada integrante deve confirmar o próprio texto antes de apresentá-lo como verificação individual.**

| Integrante | Permitida na véspera | Proibida por tempo | Proibida por consequência da decisão |
|---|---|---|---|
| Letícia | Dia da semana de `D`: calendário já conhecido. | `tipo_liberacao` em `D`: só surge no acesso. | Quantidade preparada para `D`: é decisão de produção, não demanda; ausente do mock. |
| Bianca | Tipo de refeição de `D`: planejado antes. | Refeições servidas em `D`: alvo futuro. | Sobras de `D`: dependem do preparo; ausentes do mock. |
| Kaio | Refeições de `D-7`: históricas, se a extração já fechou. | Frequência final do período: inclui aulas futuras. | Quantidade preparada para `D`: consequência da decisão; ausente do mock. |
| Dionila | Refeições de `D-7`: históricas sob atualização diária. | Refeições servidas em `D`: ainda não observadas. | Sobras de `D`: consequência do preparo; ausentes do mock. |

Também há vazamento de partição se estatísticas, codificação ou escolha de baseline forem ajustadas com validação/teste. Esse risco foi tratado pelo `fit` exclusivo no treino e pelo teste reservado.

## 6. Reprodutibilidade, contribuições e limites

O notebook executa em ordem e grava `base_analitica_diaria_curso.csv`, `base_analitica_diaria.csv`, `resultados_baselines_validacao_por_curso.csv` e `resultados_baselines_total_diario.csv` em `dados/processado/`. Essa pasta é reconstruída pela execução e ignorada pelo Git. O `requirements.txt` fixa as dependências. Nenhuma base real, dado pessoal ou credencial foi incluído.

| Pessoa | Contribuição inicial verificável | Consolidação coletiva |
|---|---|---|
| Bianca Lavine | PR #3: associação de eventos, base diária e relatório individual. | A base por curso e a regra de cobertura foram revistas pela coordenação. |
| Kaio Vitor | PR #4: auditoria, partição e vazamento. | Verificações essenciais e relatório de qualidade foram integrados pela coordenação. |
| Maria Dionila | PR #5: média, D-7 e métricas. | Baselines por curso, recorte de dias abertos e limites de interpretação foram integrados pela coordenação. |
| Letícia Braz | Contrato, mock e coordenação. | Consolidação do notebook, documentação e validação final, com apoio de Codex. |

**IA generativa:** Kaio informou Claude no PR #4; Dionila informou Claude no PR #5. A coordenação usou Codex (OpenAI) na redação e revisão do contrato, código de auditoria, cobertura, partição, pré-processamento, baselines, relatório e documentação desta E04. Bianca não declarou uso de IA no PR #3; não presumimos uso nem ausência. Cada integrante deve informar, se aplicável, os blocos que sua ferramenta influenciou e conferir o próprio trabalho. A equipe responde por todos os resultados que entregar.

Ainda dependem do RU/SEBTT: calendário e completude das extrações reais, horário de decisão e atualização, regra operacional vigente, capacidade, custos/preços e autorização de cruzamento de fontes. Até lá, D-7 é uma aproximação **do piloto**, e nenhum valor ou subsídio real foi estimado. O link público do notebook/PDF e a aprovação do grupo devem ser verificados após a publicação; a existência destes arquivos locais não equivale à submissão ao professor.
