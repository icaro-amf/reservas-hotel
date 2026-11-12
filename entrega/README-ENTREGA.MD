# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos

| # | Arquivo | Defeito | Causa raiz (uma frase) |
|-|-|-|-|
| 1 | `services/currency_converter.py` | Conversão de moeda incorreta | `convert_to_brl` fazia transformações internas indevidas e nem sempre retornava `Decimal`. |
| 2 | `services/stay_calculator.py` | Cálculo de noites incorreto | [Descreva em uma frase o que o código fazia de errado antes, por exemplo, contava a diferença de forma inclusiva.] |
| 3 | [arquivo] | [defeito] | [causa raiz] |


## Como investiguei

1. Li o `README.md` e extraí as regras de negócio (status, noites, câmbio, exatidão e ordenação).
2. Rodei `pytest -q` e vi quais testes falhavam.
3. Usei a IA (OpenCode, Nemotron 3 Ultra 550B A55B) para gerar um plano de ação inicial.
4. Corrigi um defeito por vez e validei cada um com o teste correspondente.
5. Revisei o código e corrigi os problemas que encontrei.

## Correções em detalhe

**1. Conversão de moeda (`currency_converter.py`)**
Convertia com float e dividia pela taxa em vez de multiplicar com Decimal. Removi as transformações internas do método. Agora `convert_to_brl` calcula `amount * rate_to_brl` e retorna sempre `Decimal`. Uma moeda ausente na tabela de taxas dispara uma exceção explícita, tratada pelo CLI.
Validação: `pytest tests/test_currency.py -q` passou.

**2. Cálculo de noites (`stay_calculator.py`)**
Subtraía apenas o dia do mês (.day), o que quebrava na virada de mês/ano .Passei a usar `(checkout - checkin).days * rooms`, com o `.days` do `datetime`, assim retornando em dias corridos a diferença real entre as duas datas. A IA gerou a validação que exige check-in anterior ao check-out, e eu a revisei antes de usar.
Validação: [`pytest tests/test_nights.py -q` passou.]

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

Execução no Windows (PowerShell). A variável de ambiente é definida com `$env:`:

```powershell
$env:PYTHONPATH="src"; python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

Testes:

```bash
pytest -q
```

## Resultado do pytest

```
FAILED tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show - AssertionError: assert '120.00' == '100.00'
FAILED tests/test_top_hotels.py::test_top_hotels_are_ranked_descending - AssertionError: assert ['H04', 'H03', 'H02'] == ['H01', 'H02', 'H03']
2 failed, 3 passed in 0.52s
```

## Uso de IA

Detalhes em `uso-de-ia/declaracao.md`.

## Checklist

* \[✅] O CLI roda com Python 3.11 (`PYTHONPATH=src python -m onfly\_report ...`).
* \[ ] O comando de execução gera `output/report.json` sem erro.
* \[ ] O relatório segue o contrato acima.
* \[ ] `pytest -q` passa com os testes fornecidos.
* \[ ] `entrega/README-ENTREGA.md` preenchido.
* \[ ] Sessão + declaração apenas no caminho com IA; investigação no README-ENTREGA nos dois caminhos.
* \[ ] Repositório público no GitHub com o projeto e o link enviado.