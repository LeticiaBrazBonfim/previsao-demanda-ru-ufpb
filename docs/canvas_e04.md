# Canvas da Entrega 04 — piloto sintético

**Equipe 02.** Este Canvas adapta a Entrega 3 da equipe ao contrato diário do mock. Não descreve um sistema operacional implantado na UFPB.

| Item | Definição para a E04 | Limite a confirmar |
|---|---|---|
| Usuário e decisão | Apoiar o RU no planejamento, na véspera, da quantidade a preparar no dia seguinte por tipo de refeição **e curso**. | Confirmar com o RU quem decide, em que horário e com quais dados fechados. |
| Unidade e alvo | `data × tipo_refeicao × curso`; contagem de eventos únicos `servida`. O total do RU é derivado da soma dos cursos com cobertura completa. | Verificar se a operação real requer também unidade, turno ou outro grão. |
| População e fonte | Três CSVs fictícios que simulam catraca, vínculos acadêmicos e componentes. | Dados institucionais, chaves, cobertura e autorização ainda indisponíveis. |
| Horizonte e corte | Previsão diária para `D`, calculada ao fim de `D-1`. | Conferir latência de catraca e calendário. |
| Capacidade `k` | Não quantificada na documentação recebida. | Obter capacidade de produção/atendimento por refeição, se aplicável à decisão. |
| Benefício `B` e custo `C` | Não quantificados. Subestimar pode prejudicar atendimento; superestimar pode gerar desperdício ou mau planejamento. | Levantar custos e efeitos reais antes de otimizar financeiramente ou propor subsídios. |
| Métrica inicial | MAE em refeições por `dia × tipo × curso`; RMSE e o erro do total diário complementam a leitura. Avaliar só dias abertos e completos. | Sem `k`, `B` e `C` confiáveis, MAE não equivale a custo econômico ótimo. |
| Baselines | Média por curso e tipo aprendida no treino; `D-7` por curso e tipo como heurística proposta e avaliada diariamente. | A regra atual do RU não foi confirmada; `D-7` não pode ser chamada de prática atual. |
| Partição | Treino 2019–2024, validação 2025, teste reservado 2026. | Reavaliar cortes quando houver dados reais e data de implantação. |
| Valor em R$ | A Entrega 3 registra aproximadamente R$ 16/refeição como hipótese. O mock não tem preço nem valor observado; a coluna `valor_observado` fica vazia. | Se o dado real trouxer valor por evento servido, confirmar sua semântica e vigência antes de somar por curso. Nenhuma economia ou elegibilidade é estimada nesta E04. |

O mock gera zeros conhecidos, inclusive aos domingos. O notebook avalia apenas dias abertos. Em dados reais, uma combinação sem registro só vira zero após confirmação da integridade da extração e da cobertura do curso naquele dia; caso contrário, o alvo fica vazio e não participa das métricas.
