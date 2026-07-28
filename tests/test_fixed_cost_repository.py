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

def test_copy_fixed_costs_to_another_month(repository:FixedCostRepository) -> None:
    rent = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    accounting = FixedCost(name="Księgowość", amount=1_000.0, category=CostCategory.ADMINISTRATION, year=2026, month=7)

    repository.add(rent)
    repository.add(accounting)

    copied_count = repository.copy_to_month(source_year=2026, source_month=8)
    copied_cost = repository.get_by_month(year=2026, month=8)

    assert copied_count == 2
    assert len(copied_count) == 2
    assert copied_costs[0].id is not None
    assert copied_costs[0].month == 8
    assert copied_costs[1].month == 8

def test_copy_to_same_month_raises_error(repository: FixedCostRepository) -> None:
    cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)

    repository.add(cost)

    with pytest.raises(ValueError, match=("Miesiąc źródłowy i docelowy nie mogą być takie same")):
        repository.copy_to_month(source_year=2026, source_month=7, target_year=2026, target_month=7)

def test_copy_to_non_empty_month_raices_error(repository:FixedCostRepository) -> None:
    july_cost = FixedCost(name="Czynsz", amount=10_000.0, category=CostCategory.RENT, year=2026, month=7)
    august_cost = FixedCost(name="Marketing", amount=2_000.0, category=CostCategory.MARKETING, year=2026, month=8)

    repository.add(july_cost)
    repository.add(august_cost)

    with pytest.raises(ValueError, match="miesiąc docelowy zawiera już koszty"):
        repository.copy_to_month(source_year=2026, source_month=7, target_year=2026, target_month=8)