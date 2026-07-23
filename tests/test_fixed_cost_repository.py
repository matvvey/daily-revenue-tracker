from pathlib import Path
import pytest
from costs_manager.models import CostCategory, FixedCost
from costs_manager.repository import FixedCostRepository

@pytest.fixture
def repository(tmp_path: Path) -> FixedCostRepository:
    database_path = tmp_path / "test.db"
    repository = FixedCostRepository(database_path=database_path)
    repository.initialize_table()

    return repository

def test_add_and_get_fixed_costs(repository:FixedCostRepository) -> None:
    cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    saved_cost = repository.add(cost)

    costs = repository.get_by_month(year=2026, month=7)

    assert saved_cost.id is not None
    assert len(costs) == 1
    assert costs[0] == saved_cost


def test_get_by_month_returns_only_matching_costs(repository:FixedCostRepository) -> None:
    july_cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)
    august_cost = FixedCost(name="Czynsz", amount=10_500.0, category=CostCategory.RENT, year=2026, month=8)

    repository.add(july_cost)
    repository.add(august_cost)

    july_costs = repository.get_by_month(year=2026, month=7)

    assert july_costs == [july_cost]

def test_update_fixed_cost(repository: FixedCostRepository) -> None:
    cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    repository.add(cost)
    cost.amount = 10_500.0
    cost.notes = "Podwyżka czynszu"

    repository.update(cost)

    costs = repository.get_by_month(year=2026, month=7)

    assert len(costs) == 1
    assert costs[0].amount == 10_500.0
    assert costs[0].notes == "Podwyżka czynszu"

def test_delete_fixed_costs(repository:FixedCostRepository) -> None:
    cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    repository.add(cost)
    assert cost.id is not None

    repository.delete(cost.id)
    costs = repository.get_by_month(year=2026, month=7)

    assert costs == []

def test_update_cost_without_id_raises_error(repository: FixedCostRepository) -> None:
    cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    with pytest.raises(ValueError, match="Nie można zaktualizować kosztu bez ID"):
        repository.update(cost)