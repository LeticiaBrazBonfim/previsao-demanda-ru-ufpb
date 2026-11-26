# Previsão de demanda do RU/UFPB — piloto sintético

Este repositório prepara um método para estimar, **na véspera**, quantas refeições serão servidas no dia seguinte por **tipo de refeição e curso**. O total do RU é a soma dos cursos com cobertura completa. A Entrega 04 usa somente dados **inteiramente sintéticos**. Os dados institucionais da UFPB ainda não foram recebidos, e as métricas não descrevem o RU real.

## Entrega 04

O notebook principal é [`notebooks/E04_equipe02_dados_baseline.ipynb`](notebooks/E04_equipe02_dados_baseline.ipynb). Ele lê três CSVs brutos, audita chaves e cobertura, constrói a base diária **por curso**, separa treino (até 2024), validação (2025) e teste reservado (2026), ajusta o pré-processamento **somente no treino** e mede dois baselines na validação. O `D-7` é uma heurística proposta; ainda não há confirmação de que seja a regra atual do RU.

- [`docs/contrato_previsao_mock.md`](docs/contrato_previsao_mock.md): alvo, grão, corte temporal e limites.
- [`docs/dicionario_mock.md`](docs/dicionario_mock.md): campos e categorias dos CSVs.
- [`docs/canvas_e04.md`](docs/canvas_e04.md): decisão, capacidade e custos ainda não quantificados.
- [`docs/memoria_escuta_e04.md`](docs/memoria_escuta_e04.md): proveniência e questões pendentes da escuta.
- [`docs/relatorio_qualidade_e04.md`](docs/relatorio_qualidade_e04.md): problemas, decisões, reconciliações e métricas.
- [`output/pdf/E04_equipe02_dados_baseline.pdf`](output/pdf/E04_equipe02_dados_baseline.pdf): relatório final em PDF; reproduzido por `src/gerar_relatorio_pdf_e04.py`.

As contribuições individuais estão documentadas nos PRs [#3 (Bianca)](https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb/pull/3), [#4 (Kaio)](https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb/pull/4) e [#5 (Dionila)](https://github.com/LeticiaBrazBonfim/previsao-demanda-ru-ufpb/pull/5). Seus notebooks estão em [`notebooks/individuais/`](notebooks/individuais/README.md) como registro de contribuição; **não substituem** o notebook coletivo acima.

## Entregas 05 e 06

- [`notebooks/E05_equipe02_pacote_a1.ipynb`](notebooks/E05_equipe02_pacote_a1.ipynb): baselines, Ridge, validação temporal, comparação e resíduos.
- [`output/pdf/E05_equipe02_pacote_a1.pdf`](output/pdf/E05_equipe02_pacote_a1.pdf): relatório final da E05, com uma página.
- [`notebooks/E06_equipe02_relatorio_preliminar.ipynb`](notebooks/E06_equipe02_relatorio_preliminar.ipynb): D-7, Ridge, árvore e Random Forest, seleção de hiperparâmetros e análise de erros.
- [`output/pdf/E06_equipe02_relatorio_preliminar.pdf`](output/pdf/E06_equipe02_relatorio_preliminar.pdf): relatório preliminar da E06, com duas páginas.
- [`docs/relatorio_consolidacao_e05_e06.md`](docs/relatorio_consolidacao_e05_e06.md): situação objetiva de cada contribuição e correções aplicadas.

Na validação de 2025, o Ridge foi selecionado provisoriamente com MAE 1,703 e RMSE 2,238. O resultado vale apenas para o mock. O teste de 2026 havia sido consultado numa contribuição individual da E05; a E06 não o reutiliza e registra essa limitação.

## Reproduzir

Na raiz do projeto, com Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Abra o notebook principal e use **Restart Kernel and Run All Cells**. Para executar sem interface:

```powershell
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute notebooks\E04_equipe02_dados_baseline.ipynb --output E04_equipe02_dados_baseline.executed.ipynb --output-dir notebooks
```

O notebook grava quatro arquivos reproduzíveis em `dados/processado/`: `base_analitica_diaria_curso.csv` (principal), `base_analitica_diaria.csv` (total do RU), `resultados_baselines_validacao_por_curso.csv` e `resultados_baselines_total_diario.csv`. Essa pasta é ignorada pelo Git; as saídas são reconstruídas pela execução. Os três CSVs de entrada em `dados/bruto/mock/` são preservados. Para regenerá-los com a semente fixa, execute `src/gerar_mock_diario.py` após instalar as dependências.

Para dados reais, a primeira célula de código contém `MODO`, `BRUTOS`, `COBERTURA_REAL`, `COLUNA_VALOR_EVENTO` e os cortes de data. Além de adaptar o esquema, prepare `cobertura_real.csv` com `data`, `tipo_refeicao`, `curso`, `aberto` e `extracao_completa` (`sim`/`nao`), uma linha por curso ativo e refeição em cada data. **Sem comprovação de cobertura, ausência de evento não vira zero.** Não coloque arquivos institucionais em `dados/bruto/mock/` nem os publique no repositório.

Para reconstruir o relatório PDF a partir do Markdown: `.\.venv\Scripts\python.exe src\gerar_relatorio_pdf_e04.py`.

Para executar e reconstruir as entregas mais recentes:

```powershell
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute notebooks\E05_equipe02_pacote_a1.ipynb --output E05_equipe02_pacote_a1.ipynb --output-dir notebooks
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute notebooks\E06_equipe02_relatorio_preliminar.ipynb --output E06_equipe02_relatorio_preliminar.ipynb --output-dir notebooks
.\.venv\Scripts\python.exe src\gerar_relatorios_pdf_e05_e06.py
```

## Limites

O mock simplifica calendário, cursos, comportamento e eventos. Domingos e outras combinações sem evento são zeros conhecidos **nesta simulação**; as métricas usam somente dias abertos. Dados reais exigem confirmação de dias fechados, cursos ativos e falhas de registro. O mock não possui valor monetário; `valor_observado` fica vazio. O preço por refeição, o custo real, a regra de planejamento atual e a disponibilidade dos dados na véspera ainda precisam de validação institucional. A previsão não decide subsídio individual.
