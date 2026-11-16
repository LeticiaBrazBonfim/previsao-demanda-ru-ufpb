# Integridade dos dados sintéticos

Verificação dos três CSVs brutos gerados com a semente fixa do script. Esta conferência trata apenas do mock; não inclui base analítica, baselines ou métricas de previsão.

| Arquivo | Linhas | Unidade observacional |
|---|---:|---|
| `estudantes.csv` | 2.016 | Vínculo acadêmico × período letivo |
| `matriculas_componentes.csv` | 5.922 | Inscrição em componente/turma × período |
| `catraca_ru.csv` | 224.880 | Tentativa de acesso ao RU |

Na catraca há **221.600** tentativas `servida` e **3.280** `negada`. A cobertura dos eventos vai de 01/01/2019 a 14/11/2026. Não foram encontrados valores ausentes nos três arquivos.

## Conferências realizadas

- As chaves `id_matricula, periodo_letivo`, `id_matricula_componente` e `id_registro_utilizacao` são únicas nos respectivos arquivos.
- Todas as inscrições em componentes correspondem a um vínculo e período existentes no cadastro.
- Todos os acessos correspondem a um `id_matricula` cadastrado. Isso **não** garante período letivo vigente na data: o gerador permite refeições em recesso e transições. A associação temporal deve conservar esses eventos sem inventar um período.
- As categorias de evento são `servida` e `negada`; as de liberação são `automatica` e `manual`; as refeições são café da manhã, almoço e jantar.
- As datas dos acessos estão dentro da cobertura declarada; faltas não excedem aulas previstas e notas finais estão na escala 0–10.
- Uma cópia temporária do gerador foi executada **sem notebook**. Seus três CSVs tiveram hashes SHA-256 idênticos aos arquivos preservados no projeto. Os arquivos originais não foram alterados nessa verificação.

Essas conferências demonstram consistência interna do mock, não plausibilidade estatística ou aderência ao funcionamento real do RU. O [contrato](contrato_previsao_mock.md) descreve as hipóteses; o [dicionário](dicionario_mock.md) descreve os campos.
