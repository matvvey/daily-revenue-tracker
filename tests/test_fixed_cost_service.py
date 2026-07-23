import pytest

from costs_manager.models import CostCategory, FixedCost
from costs_manager.service import FixedCostService

def test_get_days_in_month() -> None:
    assert FixedCostService.get_days_in_month(year=2026, month=7) == 31
    assert FixedCostService.get_days_in_month(year=2026, month=4) == 30

def test_get_days_in_leap_year_february() -> None:
    assert FixedCostService.get_days_in_month(year=2024, month=2) == 29

def test_calculate_total_fixed_costs() -> None:
    costs = [
        FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7),
        FixedCost(name="Księgowość", amount=1_000.0, category=CostCategory.ADMINISTRATION, year=2026, month=7)
    ]

    total = FixedCostService.calculate_total(costs)

    assert total == 11_000.0

def test_calculate_daily_avarage() -> None:
    costs = [
        FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7),
        FixedCost(name="Księgowość", amount=1_000.0, category=CostCategory.ADMINISTRATION, year=2026, month=7)
    ]

    average = FixedCostService.calculate_daily_average(costs=costs, year=2026, month=7)

    assert average == pytest.approx(11_000 / 31)

def test_calculate_total_empty_list() -> None:
    assert FixedCostService.calculate_total([]) == 0.0