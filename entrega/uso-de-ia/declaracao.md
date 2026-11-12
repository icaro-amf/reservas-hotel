# Declaração de uso de IA

## Ferramentas e modelos
- **OpenCode** com o modelo **Nemotron 3 Ultra 550B A55B e Big Pickle**: plano de ação, sugestões de código e orientação durante a resolução.
- **Claude (claude.ai)** com o modelo **Claude Sonnet 5.5**: escolha do nome e da descrição do repositório, e redação do prompt enviado ao OpenCode. Como utilizei o modelo de chat-bot na web, não consigo exportar o historico de conversa. Mas em geral, o uso foi literalmente para gerar prompts, corrigir textos e aprimorar todos os .md do projeto. Além disso, utilizei para conferência final de dados, se todos os outputs saim de acordo com nossos inputs.

## O que a IA fez
- O Nemotron gerou um plano de ação inicial, em passo a passo, sobre o que corrigir e me guiou durante a resolução do desafio.
- Entre as sugestões do Nemotron está a condicional que valida se o check-in é anterior ao check-out em `stay_calculator.py`.
- O Claude sugeriu o nome e a descrição do repositório, redigiu o prompt usado para pedir o plano ao Nemotron e aprimorou os .md do que foi implementado no projeto.

## O que eu fiz
- Corrigi `convert_to_brl` (`currency_converter.py`): a função passou a multiplicar o valor pela taxa e a retornar sempre `Decimal`, e tratei a moeda sem taxa na tabela com uma exceção explícita.
- Corrigi `stay_calculator.py` para calcular as noites com `(checkout - checkin).days * rooms`, e revisei e integrei a validação de check-in anterior ao check-out gerada pela IA.
- Revisei as sugestões de código da IA e corrigi os erros que encontrei (uso de `float`, tupla retornada por engano e `try/except` genérico).
- Corrigi `status_policy` (`status_policy.py`): `is_billable` passou a retornar `True` apenas para `CONFIRMED`, excluindo `CANCELLED` e `NO_SHOW` dos totais financeiros e de noites.
- Corrigi o ranking de `top_hotels` (`report_builder.py`): a ordenação passou a ser por valor decrescente, com desempate por `hotel_id` ascendente.
- Removi o limite fixo de 200 linhas em `csv_reservation_repository.py`, que truncava a leitura do CSV; o relatório agora lê as 300 reservas do arquivo.
- Validei cada correção com o `pytest` e com a amostra de validação.
- Preenchi o `entrega/README-ENTREGA.md` e publiquei o projeto no GitHub.

## Observações
- Nenhum teste fornecido foi alterado, e os arquivos `data/reservas_hoteis.csv` e `data/taxas_cambio.csv` permaneceram intactos.
- A conversa com o Claude na web não pôde ser exportada; o uso está resumido nesta declaração.