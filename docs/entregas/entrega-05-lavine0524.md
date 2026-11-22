# Relatório Individual — Entrega 05

## 1. Identificação

- **Nome:** Bianca Lavine
- **Usuário GitHub:** lavine0524
- **Número da entrega:** Entrega 05
- **Branch:** entrega-05-lavine0524
- **Repositório:** [LeticiaBrazBonfim/previsao-demanda-ru-ufpb](https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb)

## 2. Atividades realizadas

- Inspecionei a versão coletiva do notebook em develop/mock e a base diária processada da Entrega 4.
- Organizei as entradas em variáveis numéricas derivadas do calendário (dia_semana, mes) e categóricas (tipo_refeicao, curso); quantidade_servida permanece como alvo.
- Encapsulei imputação, padronização, codificação e RandomForestRegressor em um único Pipeline.
- Configurei o ajuste do pipeline somente com o treino. Validação recebe previsão; o teste recebe somente transformação e permanece reservado.
- Documentei que aberto filtra dias elegíveis com base no calendário de cobertura e que cadastro_cursos é usado somente na auditoria de consistência, não como preditora.
- Fixei a semente do estimador em 2026 e registrei os parâmetros aprendidos pelo pré-processamento.

## 3. Arquivos criados ou modificados

- notebooks/E04_equipe02_dados_baseline.ipynb: preparação e pipeline de regressão da E5.
- docs/entregas/entrega-05-lavine0524.md: este relatório individual.

## 4. Metodologia

O ColumnTransformer aplica imputação pela mediana e StandardScaler às variáveis numéricas de calendário. Para tipo_refeicao e curso, aplica imputação pela moda e OneHotEncoder(handle_unknown="ignore"). Essas transformações e o Random Forest são encapsulados em Pipeline, ajustado apenas com as datas de treino.

O conjunto de validação recebe previsões para uso na comparação coletiva. O conjunto de teste não é usado para ajuste nem para métricas nesta etapa. O estimador Random Forest foi usado como proposta de trabalho e deve permanecer alinhado à decisão final da equipe.

## 5. Testes e verificações

- O notebook JSON foi validado e a sintaxe Python das cinco células de código foi conferida.
- Executei sequencialmente as células de código do notebook no ambiente virtual do projeto; todas concluíram sem erro.
- A divisão resultou em 33.822 linhas de treino, 5.634 de validação e 4.914 de teste. O pré-processador produziu 11 atributos, aprendeu medianas [2, 7] e as categorias de refeição e curso somente no treino.
- O Random Forest gerou 5.634 previsões na validação. O teste foi transformado, sem gerar previsões nem métricas nesta etapa. A comparação das métricas do modelo e dos baselines permanece com a atividade coletiva designada.
- A dependência scikit-learn==1.9.1 já consta no requirements.txt da develop/mock e foi instalada no ambiente virtual local.

## 6. Limitações e pendências

- Confirmar com a equipe que RandomForestRegressor é o estimador final escolhido.
- Executar o notebook integralmente e comparar o modelo e os baselines na mesma partição de validação antes da entrega.
- O mock é sintético; os resultados não representam o desempenho do RU real.

## 7. Uso de IA generativa

Codex (OpenAI) auxiliou na inspeção do notebook, na estruturação do ColumnTransformer e do Pipeline, na redação da documentação e na revisão das variáveis para evitar vazamento. A autora deve revisar e ser capaz de explicar todo o código submetido.
