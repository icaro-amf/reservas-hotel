"""Conversão de valores para BRL."""

from __future__ import annotations

from decimal import Decimal

from onfly_report.exceptions import DataValidationError


def convert_to_brl(amount: Decimal, currency: str, rates: dict[str, Decimal]) -> Decimal:
    """Converte um valor na moeda informada para BRL usando a taxa da tabela."""
    try:
        rate = rates[currency]
        result = amount * rate
    except KeyError:
        raise DataValidationError(f"Moeda sem taxa de {currency}.")
    return result
