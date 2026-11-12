# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos

| # | Arquivo | Defeito | Causa raiz (uma frase) |
|-|-|-|-|
| 1 | `services/currency_converter.py` | Conversão de moeda incorreta | `convert_to_brl` dividia o valor pela taxa e passava por `float`, em vez de multiplicar `amount * rate` com `Decimal`. |
| 2 | `services/stay_calculator.py` | Cálculo de noites incorreto | O cálculo usava o dia do mês (`.day`) de cada data, então a diferença ignorava mês e ano. |
| 3 | `services/status_policy.py` | `NO_SHOW` entrava nos totais financeiros | `is_billable` considerava faturável qualquer status diferente de `CANCELLED`, incluindo `NO_SHOW`. |
| 4 | `services/report_builder.py` | Ranking `top_hotels` invertido | O `sorted` ordenava por valor crescente, mostrando os menores valores primeiro em vez dos maiores. |
| 5 | `repositories/csv_reservation_repository.py` | Leitura truncada em 200 linhas | A leitura do CSV tinha um `break` fixo em 200 linhas, descartando as 100 reservas restantes do arquivo. |

## Como investiguei e abordei

1. Li o `README.md` e extraí as regras de negócio (status, noites, câmbio, exatidão e ordenação).
2. Rodei `pytest -q` e usei as falhas para localizar os defeitos de câmbio, noites e status.
3. Comparei a saída da amostra `data/exemplo-validacao.csv` com a tabela de validação do README; isso expôs o ranking invertido de `top_hotels`.
4. Comparei o total de reservas do relatório com o número de linhas do CSV (300) e encontrei o limite fixo de 200 na leitura.
5. Corrigi um defeito por vez e validei cada um com o teste correspondente e com a amostra.
6. Usei IA (OpenCode/Nemotron) para o plano de ação inicial e revisei todas as sugestões antes de aplicar.

## Correções em detalhe

**1. Conversão de moeda (`currency_converter.py`)**
O código original fazia `Decimal(str(float(amount) / float(rate)))`, ou seja, dividia pela taxa e passava por `float`. Agora `convert_to_brl` multiplica `amount * rate_to_brl` e retorna `Decimal`; moeda ausente na tabela gera uma exceção explícita.
Validação: `pytest tests/test_currency.py -q` passou.

**2. Cálculo de noites (`stay_calculator.py`)**
O código original usava `(checkout.day - checkin.day) * rooms`, que compara apenas o dia do mês. Agora usa `(checkout - checkin).days * rooms`, com validação de que o check-in é anterior ao check-out.
Validação: `pytest tests/test_nights.py -q` e `pytest tests/test_regression_report.py -q` passaram.

**3. Política de status (`status_policy.py`)**
`is_billable` retornava `status != "CANCELLED"`, então `NO_SHOW` entrava nos totais. Agora retorna `status == "CONFIRMED"`; `CANCELLED` e `NO_SHOW` contam apenas nas contagens por status.
Validação: `pytest tests/test_status_rules.py -q` passou.

**4. Ranking de hotéis (`report_builder.py`)**
O ranking era ordenado por valor crescente. Agora ordena por valor decrescente e desempata por `hotel_id` ascendente: `key=lambda item: (-item[1]["amount"], item[0])`.
Validação: `pytest tests/test_top_hotels.py -q` passou e a amostra devolve `H01, H02, H12, H10, H09`.

**5. Leitura do CSV (`csv_reservation_repository.py`)**
A leitura parava em 200 linhas por causa de um `if len(rows) == 200: break`. Removi o limite; o relatório agora lê as 300 reservas do arquivo.
Validação: no dataset real, `total_reservations = 300` (235 `CONFIRMED`, 31 `CANCELLED`, 34 `NO_SHOW`).

## Como validar

Instalação:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Execução no Linux/macOS:

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

Execução no Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

Testes:

```bash
pytest -q
```

Amostra de validação (deve reproduzir a tabela do README raiz):

```bash
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

Resultado esperado: `12` reservas, `9` confirmadas, `28` noites, `7566.00` BRL; `by_month` 2025-01 (8/25/6684.00) e 2025-02 (1/3/882.00); `top_hotels` H01, H02, H12, H10, H09.

## Resultado do pytest

```
.....                                                                    [100%]
5 passed in 0.66s
```

## Uso de IA

Detalhes em `uso-de-ia/declaracao.md`.

## Checklist

- [x] O CLI roda com Python 3.11 (`PYTHONPATH=src python -m onfly_report ...`).
- [x] O comando de execução gera `output/report.json` sem erro.
- [x] O relatório segue o contrato acima.
- [x] `pytest -q` passa com os testes fornecidos.
- [x] `entrega/README-ENTREGA.md` preenchido.
- [ ] Sessão + declaração apenas no caminho com IA; investigação no README-ENTREGA nos dois caminhos.
- [ ] Repositório público no GitHub com o projeto e o link enviado.
