# Memória de escuta usada na Entrega 04

Esta memória resume a **Entrega 3 fornecida pela equipe** e explicita o que a E04 assumiu para trabalhar com dados sintéticos. Não há ata ou transcrição adicional que confirme regras operacionais do RU.

## Problema relatado na Entrega 3

A equipe descreveu uma diferença entre a estimativa teórica de refeições e o consumo variável observado nas catracas. O projeto pretende apoiar planejamento do RU e análise de recursos, com refeições separadas em café da manhã, almoço e jantar e detalhamento por curso. A Entrega 3 menciona aproximadamente R$ 16 por refeição como hipótese de referência, sem prova de valor contratual vigente. A possível ampliação de subsídio é uma questão de gestão, não uma decisão que uma previsão de demanda possa tomar sozinha.

## Tradução provisória para o mock

- Previsão diária em `D-1` para a quantidade servida em `D` por tipo de refeição **e curso**. O total do RU é derivado dos cursos. A escolha diária substitui, para este piloto, o grão mensal de um pacote antigo da E04 e precisa ser confirmada com o demandante.
- Três fontes totalmente fictícias testam chaves, agregação, partição temporal e baselines. Não representam consumo, cadastro nem contrato da UFPB.
- O calendário do gerador tem abertura de segunda a sábado, cobertura completa e seis cursos ativos no período. Zero sem evento só é conhecido nessas condições. Dados reais exigem calendário e comprovação da completude de cada extração; dias incertos ficam sem alvo.
- O histórico de 2019–2024 é treino, 2025 é validação e 2026 fica reservado. A Entrega 3 apontava 2025 como base histórica e 2026 para teste; usar anos anteriores do mock amplia o treino para esta simulação e não muda o caráter reservado de 2026.

## Perguntas ainda abertas para RU e SEBTT

1. Em que horário se decide a produção de `D` e quando a catraca de `D-1` fica completa?
2. Qual regra ou estimativa orienta a produção atualmente? O `D-7` é apenas uma aproximação proposta.
3. Que dias e refeições são efetivamente ofertados, e como distinguir fechamento de falha de registro?
4. Há identificador comum, cobertura histórica e autorização para associar catraca e dados acadêmicos?
5. Que preço ou custo por refeição se aplica a cada tipo, com qual vigência? Qual é a capacidade `k` e quais são os custos de falta e sobra?
6. Que análise de subsídio é autorizada, sem transformar previsão de consumo em decisão automática de elegibilidade?

Até essas respostas, métricas e cenários desta E04 são resultados **do mock**. Nenhum resultado deve ser apresentado como economia efetiva ou capacidade adicional de subsídio na UFPB.
