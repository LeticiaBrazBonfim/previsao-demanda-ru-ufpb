# Mock de dados — demanda do RU/UFPB

Esta etapa fornece dados **inteiramente sintéticos** para o projeto de previsão de demanda do RU do Campus III. O projeto pretende prever, na véspera, o total de refeições do dia seguinte por tipo de refeição, com curso como detalhamento. Os dados institucionais solicitados ainda não foram recebidos.

## Estrutura atual

- `src/gerar_mock_diario.py`: gera o mock com semente fixa e verificações básicas de chaves.
- `dados/bruto/mock/catraca_ru.csv`: uma tentativa de acesso por linha.
- `dados/bruto/mock/estudantes.csv`: um vínculo acadêmico por período letivo.
- `dados/bruto/mock/matriculas_componentes.csv`: uma matrícula em componente por período.
- `docs/contrato_previsao_mock.md`: objetivo, estrutura e hipóteses do mock.
- `docs/dicionario_mock.md`: campos, categorias, chaves e limitações.
- `docs/relatorio_qualidade_mock.md`: conferências básicas dos três CSVs.

`notebooks/` e `dados/processado/` permanecem vazias para as próximas etapas previstas no guia do professor. A Entrega 4 será desenvolvida posteriormente a partir dos três CSVs brutos. `docs_agente/` guarda os materiais de referência locais e permanece fora do Git.

## Reproduzir os CSVs

Na raiz do repositório, com Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\gerar_mock_diario.py
```

Se `.venv` já existir, use apenas os dois últimos comandos. O gerador grava os três CSVs em `dados/bruto/mock/` independentemente do diretório de onde é chamado. A mesma semente gera o mesmo conteúdo. Os identificadores devem ser lidos como texto para preservar zeros à esquerda.

O script não faz auditoria da Entrega 4, construção de base analítica, partição temporal ou modelagem. Os dados são fictícios; não representam utilização nem despesa observada da UFPB.
