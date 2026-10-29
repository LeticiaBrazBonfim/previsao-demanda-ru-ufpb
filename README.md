# Projeto Aplicado: Previsão de Demanda do Restaurante Universitário (RU - UFPB)

## Visão Geral
Este projeto tem como objetivo estimar o consumo e a frequência de refeições no Restaurante Universitário (RU) da UFPB para os estudantes das Escolas Técnicas, apoiando a alocação de subsídios e planejamento operacional.

## Estrutura do Repositório
- `dados/bruto/`: Dados originais e/ou base sintética gerada para testes do pipeline.
- `dados/processado/`: Base analítica limpa, transformada e pronta para modelagem.
- `notebooks/`: Análises exploratórias, auditorias e validação de baselines.
- `src/`: Scripts Python reutilizáveis (geração de dados sintéticos, limpeza e pipeline).
- `docs/`: Canvas de ML, memórias de escuta e especificações técnicas.

## Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Gere os dados sintéticos operacionais: `python src/dados.py`
3. Execute o notebook em `notebooks/` para rodar a auditoria, partição e baseline.
