"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date

from onfly_report.exceptions import DataValidationError


def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos."""
    if checkin >= checkout:
        raise DataValidationError(f"Check-in ({checkin}) deve ser anterior ao check-out ({checkout})")
    
    difference = ((checkout - checkin).days) * rooms    
    return difference
