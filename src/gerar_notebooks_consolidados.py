"""Gera os notebooks coletivos das Entregas 05 e 06."""

from pathlib import Path

import nbformat as nbf


RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOKS = RAIZ / "notebooks"


def markdown(texto: str):
    """Cria uma célula Markdown."""
    return nbf.v4.new_markdown_cell(texto.strip())


def codigo(texto: str):
    """Cria uma célula de código ainda não executada."""
    return nbf.v4.new_code_cell(texto.strip())


def gerar_e05() -> None:
    """Transforma a entrega completa de regressão em notebook coletivo da E05."""
    origem = NOTEBOOKS / "individuais" / "entrega-05-mariadionila.ipynb"
    notebook = nbf.read(origem, as_version=4)
    notebook.cells[0] = markdown(
        """
# Entrega 05 — pacote A1: baselines e primeiro modelo

**Equipe 02:** Letícia Braz, Bianca Lavine, Kaio Vitor e Maria Dionila  
**Dados:** exclusivamente sintéticos; os resultados não descrevem o RU real.

Este notebook coletivo consolida a E05. Ele refaz a base, preserva a divisão
temporal da E04, executa os baselines, ajusta um Ridge dentro de
`Pipeline`/`ColumnTransformer` e compara tudo nas mesmas linhas da validação de
2025. O teste de 2026 já foi consultado na contribuição individual de Maria;
por transparência, os resultados permanecem registrados, mas não podem mais
ser tratados como uma avaliação final totalmente intocada.
        """
    )
    notebook.cells.append(
        markdown(
            """
## 10. Consolidação e autoria

- **Maria Dionila:** baselines, Ridge, validação cruzada por datas inteiras,
  quadro comparativo e diagnóstico de resíduos. Entrega individual completa.
- **Bianca Lavine:** Random Forest exploratório e conferência do pipeline. O
  modelo permanece no notebook individual porque a E05 exige um primeiro
  modelo e o coletivo adotou o Ridge para a comparação principal; o conteúdo
  que havia sido colocado dentro da E04 foi separado para não alterar uma
  entrega já concluída.
- **Kaio Vitor:** verificação de vazamento, partição temporal e análise dos
  resíduos dos baselines. A parte dependente do modelo foi completada neste
  notebook coletivo com as previsões do Ridge.
- **Letícia Braz:** coordenação, correções e consolidação final.

**Uso de IA generativa:** Claude foi declarado por Maria e Kaio; Codex foi
declarado por Bianca e também auxiliou a coordenação na revisão, separação das
entregas e consolidação. A equipe deve conferir os resultados e conseguir
explicar o código.
            """
        )
    )
    destino = NOTEBOOKS / "E05_equipe02_pacote_a1.ipynb"
    nbf.write(notebook, destino)


def gerar_e06() -> None:
    """Gera o notebook coletivo e reproduzível da E06."""
    notebook = nbf.v4.new_notebook()
    notebook.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata["language_info"] = {"name": "python", "version": "3"}
    notebook.cells = [
        markdown(
            """
# Entrega 06 — pacote A2: seleção de modelos e relatório preliminar

**Equipe 02:** Letícia Braz, Bianca Lavine, Kaio Vitor e Maria Dionila  
**Objetivo:** prever, na véspera, refeições servidas por
`data × tipo_refeicao × curso`.

O notebook usa somente o mock. Ele compara o baseline operacional D-7 com três
candidatos: Ridge, árvore de decisão e Random Forest. A escolha de parâmetros
usa validação cruzada temporal apenas dentro do treino (2019–2024); a comparação
final usa as mesmas 5.634 linhas de 2025. O teste de 2026 não é reavaliado aqui.
            """
        ),
        markdown(
            """
## 1. Decisão, formulação e dados

A previsão apoia o planejamento diário de produção. O alvo é a quantidade de
eventos `servida`; eventos negados não entram. O total do RU é a soma dos cursos
somente quando a cobertura está completa. No mock, segunda a sábado são dias
abertos e a extração é completa. Com dados reais, calendário, cobertura,
capacidade e custos precisam ser fornecidos pelo RU.

MAE é a métrica principal porque está na unidade da decisão. RMSE é secundária
e destaca erros grandes. Como os custos de falta (`B`), sobra (`C`) e capacidade
(`k`) ainda não foram levantados, a perda é provisoriamente simétrica.
            """
        ),
        codigo(
            """
from pathlib import Path
import time

import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

RAIZ = next(
    (p for p in [Path.cwd(), *Path.cwd().parents] if (p / "dados/bruto/mock").is_dir()),
    None,
)
if RAIZ is None:
    raise FileNotFoundError("Abra o notebook dentro do repositório.")

BRUTOS = RAIZ / "dados/bruto/mock"
PROCESSADOS = RAIZ / "dados/processado"
FIGURAS = RAIZ / "output/figuras"
PROCESSADOS.mkdir(parents=True, exist_ok=True)
FIGURAS.mkdir(parents=True, exist_ok=True)

SEMENTE = 2026
FIM_TREINO = pd.Timestamp("2024-12-31")
FIM_VALIDACAO = pd.Timestamp("2025-12-31")
            """
        ),
        markdown(
            """
## 2. Pipeline reproduzível: CSV bruto → base modelável

Cada linha representa uma data, refeição e curso. As defasagens são calculadas
na grade diária completa; assim, `lag_7` significa exatamente sete dias antes.
Todas as entradas existem até D-1. O alvo do próprio dia nunca entra em `X`.
            """
        ),
        codigo(
            """
catraca = pd.read_csv(BRUTOS / "catraca_ru.csv", dtype="string")
estudantes = pd.read_csv(BRUTOS / "estudantes.csv", dtype="string")
catraca["data"] = pd.to_datetime(
    catraca["data_hora_refeicao"], errors="coerce"
).dt.normalize()

if catraca["data"].isna().any():
    raise ValueError("Há datas inválidas na catraca.")
if catraca["id_registro_utilizacao"].duplicated().any():
    raise ValueError("Há identificadores de evento duplicados.")

servidas = catraca.loc[catraca["situacao_evento"].eq("servida")].copy()
chave = ["data", "tipo_refeicao", "curso"]
contagens = (
    servidas.groupby(chave)["id_registro_utilizacao"]
    .nunique()
    .reset_index(name="quantidade_servida")
)

datas = pd.date_range("2019-01-01", "2026-11-14", freq="D")
refeicoes = sorted(catraca["tipo_refeicao"].dropna().unique())
cursos = sorted(estudantes["curso"].dropna().unique())
base = pd.MultiIndex.from_product(
    [datas, refeicoes, cursos], names=chave
).to_frame(index=False)
base["aberto"] = base["data"].dt.day_of_week.lt(6)
base["extracao_completa"] = True
base = base.merge(contagens, how="left", on=chave, validate="one_to_one")

if base.loc[~base["aberto"], "quantidade_servida"].notna().any():
    raise ValueError("O mock tem eventos em dia fechado.")

base["quantidade_servida"] = base["quantidade_servida"].fillna(0).astype(int)
assert int(base["quantidade_servida"].sum()) == len(servidas) == 221_600

base = base.sort_values(["curso", "tipo_refeicao", "data"]).reset_index(drop=True)
grupo = base.groupby(["curso", "tipo_refeicao"])["quantidade_servida"]
for atraso in (7, 14, 21, 28):
    base[f"lag_{atraso}"] = grupo.shift(atraso)

base["media_4sem"] = base[["lag_7", "lag_14", "lag_21", "lag_28"]].mean(axis=1)
base["tendencia"] = (base["data"] - pd.Timestamp("2019-01-01")).dt.days
base["dia_semana"] = base["data"].dt.day_of_week.astype(str)
base["mes"] = base["data"].dt.month.astype(str)

modelavel = base.loc[base["aberto"] & base["extracao_completa"]].copy()
modelavel = modelavel.sort_values(["data", "curso", "tipo_refeicao"]).reset_index(drop=True)
treino = modelavel.loc[modelavel["data"].le(FIM_TREINO)].copy()
validacao = modelavel.loc[
    modelavel["data"].gt(FIM_TREINO) & modelavel["data"].le(FIM_VALIDACAO)
].copy()
teste = modelavel.loc[modelavel["data"].gt(FIM_VALIDACAO)].copy()
assert treino["data"].max() < validacao["data"].min() < teste["data"].min()

print("Eventos servidos:", len(servidas))
print("Linhas treino / validação / teste:", len(treino), len(validacao), len(teste))
print("Teste identificado, mas não usado nesta entrega.")
            """
        ),
        markdown(
            """
## 3. Baselines e validação temporal

O baseline trivial é a média do treino por curso e refeição. O baseline
operacional proposto é D-7. Ele não é apresentado como regra confirmada do RU.
As cinco dobras são expansivas e formadas por datas inteiras: nenhuma data pode
ficar dos dois lados de uma dobra.
            """
        ),
        codigo(
            """
media_treino = (
    treino.groupby(["curso", "tipo_refeicao"])["quantidade_servida"]
    .mean()
    .rename("prev_trivial")
    .reset_index()
)
validacao = validacao.merge(
    media_treino, how="left", on=["curso", "tipo_refeicao"], validate="many_to_one"
)
validacao["prev_d7"] = validacao["lag_7"]
assert validacao[["prev_trivial", "prev_d7"]].notna().all().all()

NUMERICAS = ["lag_7", "media_4sem", "tendencia"]
CATEGORICAS = ["dia_semana", "mes", "tipo_refeicao", "curso"]
FEATURES = NUMERICAS + CATEGORICAS

preprocessador = ColumnTransformer(
    [
        (
            "num",
            Pipeline(
                [
                    ("imputa", SimpleImputer(strategy="median")),
                    ("escala", StandardScaler()),
                ]
            ),
            NUMERICAS,
        ),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
    ]
)

def dobras_por_data(tabela, quantidade=5):
    datas_unicas = np.sort(tabela["data"].unique())
    pedacos = np.array_split(datas_unicas, quantidade + 1)
    dobras = []
    for numero in range(1, quantidade + 1):
        datas_fit = np.concatenate(pedacos[:numero])
        datas_val = pedacos[numero]
        assert datas_fit.max() < datas_val.min()
        assert set(datas_fit).isdisjoint(set(datas_val))
        idx_fit = np.flatnonzero(tabela["data"].isin(datas_fit))
        idx_val = np.flatnonzero(tabela["data"].isin(datas_val))
        dobras.append((idx_fit, idx_val))
    return dobras

dobras = dobras_por_data(treino)
print("Dobras temporais:", len(dobras))
for numero, (idx_fit, idx_val) in enumerate(dobras, start=1):
    print(
        numero,
        treino.iloc[idx_fit]["data"].min().date(),
        "a",
        treino.iloc[idx_fit]["data"].max().date(),
        "→",
        treino.iloc[idx_val]["data"].min().date(),
        "a",
        treino.iloc[idx_val]["data"].max().date(),
    )
            """
        ),
        markdown(
            """
## 4. Três candidatos e escolha de hiperparâmetros

Cada combinação é ajustada novamente em cada dobra. Ridge representa o modelo
linear regularizado; a árvore permite regras não lineares; Random Forest é o
ensemble. As grades são pequenas para manter a execução didática e rápida.
            """
        ),
        codigo(
            """
def criar_pipeline(regressor):
    return Pipeline(
        [("preprocessador", clone(preprocessador)), ("regressor", regressor)]
    )


candidatos = {
    "Ridge": {
        "pipeline": criar_pipeline(Ridge()),
        "grade": {"regressor__alpha": [10.0, 100.0, 1000.0]},
    },
    "Árvore": {
        "pipeline": criar_pipeline(DecisionTreeRegressor(random_state=SEMENTE)),
        "grade": {
            "regressor__max_depth": [4, 8],
            "regressor__min_samples_leaf": [5, 20],
        },
    },
    "Random Forest": {
        "pipeline": criar_pipeline(
            RandomForestRegressor(
                n_estimators=100, random_state=SEMENTE, n_jobs=-1
            )
        ),
        "grade": {
            "regressor__max_depth": [8, None],
            "regressor__min_samples_leaf": [2, 10],
        },
    },
}

registros_cv = []
melhores = {}
for nome, configuracao in candidatos.items():
    inicio_busca = time.perf_counter()
    for parametros in ParameterGrid(configuracao["grade"]):
        maes = []
        rmses = []
        for idx_fit, idx_val in dobras:
            modelo = clone(configuracao["pipeline"]).set_params(**parametros)
            modelo.fit(treino.iloc[idx_fit][FEATURES], treino.iloc[idx_fit]["quantidade_servida"])
            previsao = np.maximum(modelo.predict(treino.iloc[idx_val][FEATURES]), 0)
            real = treino.iloc[idx_val]["quantidade_servida"]
            maes.append(mean_absolute_error(real, previsao))
            rmses.append(np.sqrt(mean_squared_error(real, previsao)))
        registros_cv.append(
            {
                "modelo": nome,
                "parametros": parametros.copy(),
                "MAE_cv": np.mean(maes),
                "RMSE_cv": np.mean(rmses),
            }
        )
    tempo_busca = time.perf_counter() - inicio_busca
    tabela_modelo = pd.DataFrame(registros_cv).query("modelo == @nome")
    melhor = tabela_modelo.sort_values(["MAE_cv", "RMSE_cv"]).iloc[0]
    melhores[nome] = {
        "parametros": dict(melhor["parametros"]),
        "MAE_cv": float(melhor["MAE_cv"]),
        "RMSE_cv": float(melhor["RMSE_cv"]),
        "tempo_busca": tempo_busca,
    }

cv_resultados = pd.DataFrame(registros_cv).sort_values(["modelo", "MAE_cv"])
display(cv_resultados.round(3))
            """
        ),
        markdown(
            """
## 5. Comparação final na validação de 2025

Após escolher os parâmetros somente no treino, cada candidato é reajustado em
todo o treino e aplicado uma única vez à validação. Baselines e modelos usam as
mesmas linhas e métricas.
            """
        ),
        codigo(
            """
previsoes = validacao[
    ["data", "tipo_refeicao", "curso", "quantidade_servida"]
].copy()
previsoes["Baseline trivial"] = validacao["prev_trivial"].to_numpy()
previsoes["D-7 proposto"] = validacao["prev_d7"].to_numpy()

linhas_resultado = []
modelos_finais = {}
for nome, configuracao in candidatos.items():
    parametros = melhores[nome]["parametros"]
    modelo = clone(configuracao["pipeline"]).set_params(**parametros)
    inicio_fit = time.perf_counter()
    modelo.fit(treino[FEATURES], treino["quantidade_servida"])
    tempo_fit = time.perf_counter() - inicio_fit
    previsoes[nome] = np.maximum(modelo.predict(validacao[FEATURES]), 0)
    modelos_finais[nome] = modelo
    melhores[nome]["tempo_fit"] = tempo_fit

def medir(nome, previsto, parametros, tempo_busca, tempo_fit):
    real = previsoes["quantidade_servida"]
    return {
        "abordagem": nome,
        "parametros": parametros,
        "MAE": mean_absolute_error(real, previsto),
        "RMSE": np.sqrt(mean_squared_error(real, previsto)),
        "vies_real_menos_prev": (real - previsto).mean(),
        "tempo_busca_s": tempo_busca,
        "tempo_fit_final_s": tempo_fit,
    }

linhas_resultado.append(
    medir("Baseline trivial", previsoes["Baseline trivial"], "média do treino", 0, 0)
)
linhas_resultado.append(
    medir("D-7 proposto", previsoes["D-7 proposto"], "sem ajuste", 0, 0)
)
for nome in candidatos:
    linhas_resultado.append(
        medir(
            nome,
            previsoes[nome],
            str(melhores[nome]["parametros"]),
            melhores[nome]["tempo_busca"],
            melhores[nome]["tempo_fit"],
        )
    )

comparacao = pd.DataFrame(linhas_resultado).sort_values("MAE").reset_index(drop=True)
vencedor = comparacao.loc[
    comparacao["abordagem"].isin(candidatos), "abordagem"
].iloc[0]

display(comparacao.round(3))
print("Modelo selecionado na validação:", vencedor)
print("Teste 2026 não foi usado nem avaliado na E06.")

comparacao.to_csv(PROCESSADOS / "comparacao_modelos_e06.csv", index=False)
previsoes.to_csv(PROCESSADOS / "previsoes_validacao_e06.csv", index=False)
            """
        ),
        markdown(
            """
## 6. Erros, casos críticos e equidade operacional

Resíduo positivo (`real − previsto`) indica subestimação e risco de falta;
negativo indica superestimação e risco de sobra. Curso e refeição são grupos
operacionais, não atributos protegidos. A comparação abaixo serve para localizar
falhas do modelo; não permite concluir discriminação com dados sintéticos.
            """
        ),
        codigo(
            """
diagnostico = previsoes.copy()
diagnostico["previsto"] = diagnostico[vencedor]
diagnostico["residuo"] = (
    diagnostico["quantidade_servida"] - diagnostico["previsto"]
)
diagnostico["erro_absoluto"] = diagnostico["residuo"].abs()

resumo_curso = (
    diagnostico.groupby("curso")
    .agg(
        linhas=("residuo", "size"),
        MAE=("erro_absoluto", "mean"),
        vies=("residuo", "mean"),
        subestimacoes=("residuo", lambda x: int((x > 0).sum())),
        superestimacoes=("residuo", lambda x: int((x < 0).sum())),
    )
    .sort_values("MAE", ascending=False)
)
resumo_refeicao = (
    diagnostico.groupby("tipo_refeicao")
    .agg(MAE=("erro_absoluto", "mean"), vies=("residuo", "mean"))
    .sort_values("MAE", ascending=False)
)
piores = diagnostico.nlargest(10, "erro_absoluto")[
    [
        "data",
        "curso",
        "tipo_refeicao",
        "quantidade_servida",
        "previsto",
        "residuo",
        "erro_absoluto",
    ]
]

print("Erros por curso:")
display(resumo_curso.round(3))
print("Erros por refeição:")
display(resumo_refeicao.round(3))
print("Dez casos com maior erro absoluto:")
piores_exibicao = piores.copy()
for coluna in ["previsto", "residuo", "erro_absoluto"]:
    piores_exibicao[coluna] = piores_exibicao[coluna].round(2)
display(piores_exibicao)

assert resumo_curso["linhas"].min() >= 30
            """
        ),
        markdown(
            """
## 7. Operação, produto e riscos

### Limiar e capacidade

Não há limiar de classificação porque a tarefa é regressão. A saída operacional
provisória é `max(0, arredondar(previsão))`. Não aplicamos teto: a capacidade
real (`k`) ainda não foi informada. Quando ela existir, o painel deve mostrar a
previsão sem corte, a recomendação limitada pela capacidade e um alerta de
excesso separadamente.

### Produto preliminar

```text
+--------------------------------------------------------------+
| RU/UFPB — PREVISÃO PARA AMANHÃ                               |
+--------------------------------------------------------------+
| Data [____]  Refeição [____]  Cobertura [completa/incompleta] |
| Total previsto [____]  Capacidade [a confirmar]               |
+--------------------------------------------------------------+
| Curso | previsão | histórico | faixa de erro | alerta          |
+--------------------------------------------------------------+
| Avisos: dado sintético; revisão humana obrigatória            |
+--------------------------------------------------------------+
```

Principais riscos: dados sintéticos, calendário ou cobertura errados, mudança
temporal, subestimação, sobra, capacidade/custos desconhecidos e uso indevido.
Mitigações: validação com dados reais, monitoramento por período/grupo, alerta
de cobertura, revisão humana e proibição de uso para decidir acesso ao RU.
            """
        ),
        markdown(
            """
## 8. Reprodutibilidade, limites e autoria

- Execute todas as células do início ao fim com as versões fixadas em
  `requirements.txt`.
- O teste de 2026 não é usado na E06. Porém, ele já havia sido consultado na
  contribuição individual da E05; portanto, não existe mais teste totalmente
  intocado neste mock.
- Resultados reais dependem do calendário, cobertura, cursos ativos, custos,
  capacidade e regra operacional confirmados pelo RU.

### Contribuições

- **Bianca Lavine:** base comum, protocolo temporal, D-7 e Ridge. Entrega
  individual completa para a responsabilidade atribuída.
- **Kaio Vitor:** funções e texto de análise de erros/equidade, produto,
  wireframe e riscos. Entrega individual parcial: dependia das previsões
  oficiais; a consolidação executou a análise definitiva acima.
- **Maria Dionila:** não abriu PR individual da E06 até esta consolidação. O
  Ridge e a comparação da E05 foram reaproveitados como base conceitual, mas
  não contam como entrega individual da E06.
- **Letícia Braz:** árvore de decisão, Random Forest, comparação comum,
  correções, execução e consolidação coletiva.

### IA generativa

Bianca declarou uso de Codex; Kaio declarou uso de Claude em sua documentação
anterior e sua E06 deve manter a declaração correspondente. Codex auxiliou a
coordenação na integração, revisão e consolidação. A equipe deve revisar e ser
capaz de explicar cada bloco.
            """
        ),
    ]
    destino = NOTEBOOKS / "E06_equipe02_relatorio_preliminar.ipynb"
    nbf.write(notebook, destino)


if __name__ == "__main__":
    gerar_e05()
    gerar_e06()
    print("Notebooks coletivos E05 e E06 gerados.")
