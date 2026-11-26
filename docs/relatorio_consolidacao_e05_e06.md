# Relatório de consolidação das Entregas 05 e 06

## Situação objetiva por integrante

| Integrante | E05 | E06 | O que precisou ser feito na consolidação |
|---|---|---|---|
| Maria Dionila | **Completa** | **Não entregou** | A E05 foi integrada após a correção da validação por datas inteiras. Não havia PR individual da E06. |
| Bianca Lavine | **Parcial, com correção estrutural** | **Completa** | O Random Forest da E05 foi retirado do notebook final da E04; na E06, base, Ridge e saídas estavam executados e coerentes. |
| Kaio Vitor | **Parcial** | **Parcial** | As análises que dependiam das previsões finais foram executadas no notebook coletivo. Produto, riscos e funções foram aproveitados. |
| Letícia Braz | **Coordenação/consolidação** | **Coordenação/consolidação** | Separou as entregas, implementou candidatos faltantes, comparou modelos, corrigiu documentação e gerou os produtos coletivos. |

## Correções aplicadas

- Restauração do notebook final da E04, que não deve receber código de entregas posteriores.
- Criação dos notebooks coletivos próprios da E05 e da E06.
- Comparação de todos os métodos nas mesmas linhas de 2025.
- Validação cruzada por datas inteiras, sem dividir cursos/refeições do mesmo dia entre treino e validação.
- Inclusão de Ridge, árvore e Random Forest com hiperparâmetros escolhidos somente no treino.
- Execução da análise definitiva de erros por curso, refeição e observações críticas.
- Registro explícito de que o teste de 2026 já foi consultado na E05 e não foi reutilizado na E06.
- Documentação de capacidade, custos, cobertura, limitações e uso de IA.

## Resultado coletivo

O Ridge foi selecionado provisoriamente: MAE 1,703 e RMSE 2,238 na validação de 2025. Ele superou D-7, árvore e Random Forest, além de ser o modelo mais simples e barato entre os candidatos. O resultado vale somente para o mock.
