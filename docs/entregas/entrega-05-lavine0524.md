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
- Implementei validação cruzada temporal dentro do treino, agrupando todas as linhas da mesma data no mesmo fold.
- Calculei MAE e RMSE do Random Forest na validação de 2025 e examinei os resíduos por curso e tipo de refeição.

## 3. Arquivos criados ou modificados

- notebooks/E04_equipe02_dados_baseline.ipynb: preparação e pipeline de regressão da E5.
- docs/entregas/entrega-05-lavine0524.md: este relatório individual.

## 4. Metodologia

O ColumnTransformer aplica imputação pela mediana e StandardScaler às variáveis numéricas de calendário. Para tipo_refeicao e curso, aplica imputação pela moda e OneHotEncoder(handle_unknown="ignore"). Essas transformações e o Random Forest são encapsulados em Pipeline, ajustado apenas com as datas de treino.

A validação cruzada temporal usa somente as datas de treino até 2024 e mantém as linhas de cada dia juntas. O Pipeline final é ajustado com o treino; a validação de 2025 é usada para MAE, RMSE e análise dos resíduos. O teste de 2026 fica reservado e não participa da escolha de parâmetros. A configuração do Random Forest (300 árvores) é fixa nesta versão; se houver ajuste de hiperparâmetros, ele deve ocorrer usando apenas os folds do treino.

## 5. Testes e verificações

- O notebook JSON foi validado, e a sintaxe das novas células foi conferida. Executei sequencialmente as células de código no ambiente virtual do projeto; todas concluíram sem erro.
- A divisão resultou em 33.822 linhas de treino, 5.634 de validação e 4.914 de teste. O pré-processador produziu 11 atributos, aprendeu medianas [2, 7] e as categorias de refeição e curso somente no treino.
- Na validação cruzada temporal do treino, as médias foram MAE 1,51 e RMSE 1,98. Na validação de 2025, o Random Forest obteve MAE 1,57 e RMSE 2,09 em 5.634 linhas (uma linha por data, curso e refeição).
- O maior erro médio apareceu no almoço (MAE 1,87); por curso, B e D tiveram os maiores MAEs médios (1,74 cada), enquanto E e C tiveram os menores (1,39 e 1,40). Os resíduos médios positivos indicam leve tendência de subestimar a demanda.
- O teste de 2026 foi transformado pelo pré-processador, mas não recebeu previsões ou métricas e não foi usado para escolher parâmetros.
- A dependência scikit-learn==1.9.1 já consta no requirements.txt da develop/mock e foi instalada no ambiente virtual local.

## 6. Limitações e pendências

- Confirmar com a equipe que RandomForestRegressor é o estimador final escolhido.
- Confirmar com a equipe se a configuração fixa de 300 árvores deve permanecer ou se haverá seleção de parâmetros usando somente a validação cruzada do treino.
- O mock é sintético; os resultados não representam o desempenho do RU real.

## 7. Uso de IA generativa

Codex (OpenAI) auxiliou na inspeção do notebook, na estruturação do ColumnTransformer e do Pipeline, na redação da documentação e na revisão das variáveis para evitar vazamento. A autora deve revisar e ser capaz de explicar todo o código submetido.
