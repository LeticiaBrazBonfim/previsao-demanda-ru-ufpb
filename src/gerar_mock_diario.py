"""Define as funções para gerar os três CSVs brutos do mock.

Executar este arquivo ou chamar gerar() pelo notebook grava estudantes.csv,
matriculas_componentes.csv e catraca_ru.csv em dados/bruto/mock/. Este módulo
não constrói a base analítica nem as métricas: o notebook faz essas etapas e
grava os resultados derivados em dados/processado/mock/.
"""

from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTO = RAIZ / "dados" / "bruto" / "mock"
SEMENTE = 20261001
INICIO = pd.Timestamp("2019-01-01")
FIM = pd.Timestamp("2026-11-14")
UNIDADE = "RU_CAVN_SIMULADO"


def periodos():
    for ano in range(2019, 2027):
        for semestre in (1, 2):
            inicio = pd.Timestamp(ano, 2 if semestre == 1 else 8, 1)
            if inicio > FIM:
                continue
            fim = pd.Timestamp(ano, 6 if semestre == 1 else 12, 30 if semestre == 1 else 20)
            yield f"{ano}.{semestre}", inicio, min(fim, FIM)


def criar_estudantes():
    pessoas = [(f"DIS_SIM_{n+1:04d}", f"MAT_SIM_{n+1:04d}", "2025.2" if n >= 120 else "2019.1", n % 6) for n in range(144)]
    # Doze discentes têm dois vínculos, com IDs distintos.
    pessoas += [(f"DIS_SIM_{n+1:04d}", f"MAT_SIM_{145+n:04d}", "2026.1", (n+1) % 6) for n in range(12)]
    linhas = []
    for periodo, inicio, fim in periodos():
        ano, semestre = map(int, periodo.split("."))
        recesso_inicio = pd.Timestamp(ano, 1 if semestre == 1 else 7, 1)
        recesso_fim = recesso_inicio + pd.offsets.MonthEnd(0)
        suspensao = pd.Timestamp(ano, 4 if semestre == 1 else 10, 15)
        for id_discente, id_matricula, ingresso, curso_n in pessoas:
            if ingresso > periodo:
                continue
            n = int(id_discente[-4:])
            situacao = "ativo"
            if n <= 3 and periodo == "2023.2":
                situacao = "trancado"
            if 4 <= n <= 6 and periodo >= "2024.1":
                situacao = "cancelado"
            if 7 <= n <= 9 and periodo >= "2025.2":
                situacao = "concluido"
            linhas.append({
                "id_discente": id_discente, "id_matricula": id_matricula,
                "matricula": f"{ingresso[:4]}{int(id_matricula[-4:]):06d}",
                "id_curso": f"CUR_{curso_n+1:02d}",
                "curso": f"CURSO_TECNICO_{'ABCDEF'[curso_n]}",
                "nivel_ensino": "tecnico", "id_matriz": f"MATRIZ_{curso_n+1:02d}",
                "id_curriculo": f"CURRIC_{curso_n+1:02d}",
                "periodo_ingresso": ingresso, "periodo_letivo": periodo,
                "situacao_vinculo_periodo": situacao,
                "inicio_periodo_letivo": inicio.date().isoformat(),
                "fim_periodo_letivo": fim.date().isoformat(),
                "inicio_recesso": recesso_inicio.date().isoformat(),
                "fim_recesso": recesso_fim.date().isoformat(),
                "datas_suspensao_atividades": suspensao.date().isoformat(),
                "residente": n % 4 == 0,
                "tipo_auxilio": "residencia_estudantil" if n % 4 == 0 else ("auxilio_alimentacao" if n % 3 == 0 else "sem_auxilio"),
            })
    return pd.DataFrame(linhas)


def criar_componentes(estudantes, rng):
    linhas = []
    ativos = estudantes.loc[estudantes.situacao_vinculo_periodo == "ativo"]
    for row in ativos.itertuples(index=False):
        for n, dias, inicio, fim, modalidade in (
            (1, "SEG|QUA", "08:00", "10:00", "presencial"),
            (2, "TER|QUI", "13:00", "15:00", "presencial"),
            (3, "SEX", "10:00", "12:00", "hibrida"),
        ):
            previstas = 40 if n < 3 else 20
            faltas = int(rng.integers(0, 9))
            nota = round(float(rng.uniform(4, 10)), 1)
            linhas.append({
                "id_matricula_componente": f"MC_{row.id_matricula}_{row.periodo_letivo}_{n}",
                "id_matricula": row.id_matricula, "periodo_letivo": row.periodo_letivo,
                "id_componente": f"COMP_{n:02d}",
                "componente": ("Matematica", "Agroecologia", "Projeto Integrador")[n-1],
                "id_turma": f"TURMA_{row.id_curso}_{row.periodo_letivo}_{n}",
                "dias_semana_aula": dias, "horario_inicio": inicio, "horario_fim": fim,
                "modalidade": modalidade, "local_aula": "SALA_SIM_01" if n < 3 else "LAB_SIM_01",
                "id_docente": f"DOC_SIM_{n:03d}", "docente": f"Docente ficticio {n:03d}",
                "aulas_previstas": previstas, "faltas": faltas,
                "frequencia_percentual": round(100 * (previstas - faltas) / previstas, 2),
                "nota_final": nota,
                "resultado_final": "aprovado" if nota >= 6 and faltas / previstas <= .25 else "reprovado",
            })
    return pd.DataFrame(linhas)


def criar_catraca(estudantes, componentes, rng):
    datas = pd.DataFrame({"data": pd.date_range(INICIO, FIM)})
    datas["periodo_letivo"] = datas.data.dt.year.astype(str) + "." + np.where(datas.data.dt.month <= 6, "1", "2")
    datas["dia_semana"] = datas.data.dt.day_of_week
    datas = datas.loc[datas.dia_semana < 6]
    vinculos = estudantes.loc[estudantes.situacao_vinculo_periodo == "ativo", [
        "id_discente", "id_matricula", "matricula", "id_curso", "curso", "nivel_ensino",
        "periodo_letivo", "residente", "tipo_auxilio", "inicio_periodo_letivo",
        "fim_periodo_letivo", "datas_suspensao_atividades",
    ]]
    painel = vinculos.merge(datas, on="periodo_letivo", how="inner", validate="many_to_many")
    # Quem tem dois vínculos usa apenas um por dia; os eventos mantêm o vínculo escolhido.
    painel["ordem_vinculo"] = (painel.data.dt.day_of_year + painel.id_matricula.str[-4:].astype(int)) % 2
    painel = painel.sort_values(["id_discente", "data", "ordem_vinculo", "id_matricula"])
    painel = painel.drop_duplicates(["id_discente", "data"], keep="first").copy()
    grade = componentes.groupby(["id_matricula", "periodo_letivo"]).dias_semana_aula.agg("|".join).reset_index()
    painel = painel.merge(grade, on=["id_matricula", "periodo_letivo"], how="left", validate="many_to_one")
    mapa_dias = np.array(["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"])
    painel["aula_prevista"] = [mapa_dias[d] in str(g) for d, g in zip(painel.dia_semana, painel.dias_semana_aula)]
    painel["dia_letivo"] = (
        (painel.data >= pd.to_datetime(painel.inicio_periodo_letivo))
        & (painel.data <= pd.to_datetime(painel.fim_periodo_letivo))
        & (painel.data.dt.date.astype(str) != painel.datas_suspensao_atividades)
    )
    painel["aula_prevista"] &= painel.dia_letivo
    partes = []
    for refeicao, (hora, base, efeito_aula) in {
        "cafe_da_manha": (7, .02, .18), "almoco": (12, .05, .40), "jantar": (18, .02, .15)
    }.items():
        prob = base + efeito_aula * painel.aula_prevista.to_numpy() + .23 * painel.residente.to_numpy()
        selecionados = painel.loc[rng.random(len(painel)) < prob].copy()
        sorteio = rng.random(len(selecionados))
        selecionados["situacao_evento"] = np.where(sorteio < .985, "servida", "negada")
        selecionados["data_hora_refeicao"] = (
            selecionados.data + pd.to_timedelta(hora, unit="h")
            + pd.to_timedelta(rng.integers(0, 60, len(selecionados)), unit="m")
        )
        selecionados["tipo_refeicao"] = refeicao
        selecionados["tipo_acesso"] = np.where(selecionados.tipo_auxilio == "sem_auxilio", "parcial", "total")
        selecionados["tipo_liberacao"] = np.where(rng.random(len(selecionados)) < .9, "automatica", "manual")
        partes.append(selecionados)
    catraca = pd.concat(partes, ignore_index=True).sort_values(
        ["data_hora_refeicao", "id_matricula", "tipo_refeicao"]
    ).reset_index(drop=True)
    catraca.insert(0, "id_registro_utilizacao", [f"EVT_SIM_{i:08d}" for i in range(1, len(catraca)+1)])
    catraca["unidade_ru"] = UNIDADE
    return catraca[[
        "id_registro_utilizacao", "unidade_ru", "tipo_refeicao", "tipo_acesso",
        "data_hora_refeicao", "tipo_liberacao", "nivel_ensino", "matricula",
        "id_matricula", "curso", "id_curso", "tipo_auxilio", "situacao_evento",
    ]]


def gerar():
    """Cria os registros sintéticos e grava os três CSVs brutos."""
    rng = np.random.default_rng(SEMENTE)
    estudantes = criar_estudantes()
    componentes = criar_componentes(estudantes, rng)
    catraca = criar_catraca(estudantes, componentes, rng)
    assert not estudantes.duplicated(["id_matricula", "periodo_letivo"]).any()
    assert not componentes.id_matricula_componente.duplicated().any()
    assert not catraca.id_registro_utilizacao.duplicated().any()
    BRUTO.mkdir(parents=True, exist_ok=True)
    for nome, frame in (
        ("estudantes", estudantes),
        ("matriculas_componentes", componentes),
        ("catraca_ru", catraca),
    ):
        frame.to_csv(BRUTO / f"{nome}.csv", index=False, encoding="utf-8", date_format="%Y-%m-%d %H:%M:%S")
        print(f"{nome}.csv: {len(frame)} linhas")
    return {nome: BRUTO / f"{nome}.csv" for nome in ("estudantes", "matriculas_componentes", "catraca_ru")}


if __name__ == "__main__":
    gerar()
