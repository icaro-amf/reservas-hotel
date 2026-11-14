from __future__ import annotations

from datetime import date

import pytest

from onfly_report.exceptions import DataValidationError
from onfly_report.services.stay_calculator import calculate_room_nights


def test_rejects_checkin_after_checkout():
    with pytest.raises(DataValidationError):
        calculate_room_nights(date(2025, 2, 10), date(2025, 2, 5), 1)