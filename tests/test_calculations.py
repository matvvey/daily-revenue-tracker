import pytest
from calculations import (
    calculate_choice_commission,
    calculate_marketplace_commission,
    calculate_daily_result,
    calculate_terminal_commission,
)


def test_calculate_marketplace_commission() -> None:
    result = calculate_marketplace_commission(
        uber_revenue=100,
        wolt_revenue=100,
        glovo_revenue=100,
        pyszne_revenue=100,
    )

    assert result == pytest.approx(150.0)


def test_calculate_terminal_commission() -> None:
    result = calculate_terminal_commission(
        terminal_revenue=1000,
    )

    assert result == pytest.approx(20.0)


def test_calculate_choice_commission() -> None:
    result = calculate_choice_commission(
        choice_online_revenue=1000,
    )

    assert result == pytest.approx(20.0)


def test_calculate_daily_result() -> None:
    result = calculate_daily_result(
        gross_revenue=5000,
        daily_costs=500,
        marketplace_commission=600,
        terminal_commission=50,
        choice_commission=30,
    )

    assert result == pytest.approx(3820.0)


def test_all_commissions_are_zero_when_revenue_is_zero() -> None:
    marketplace_commission = calculate_marketplace_commission(
        uber_revenue=0,
        wolt_revenue=0,
        glovo_revenue=0,
        pyszne_revenue=0,
    )

    terminal_commission = calculate_terminal_commission(
        terminal_revenue=0,
    )

    choice_commission = calculate_choice_commission(
        choice_online_revenue=0,
    )

    assert marketplace_commission == pytest.approx(0.0)
    assert terminal_commission == pytest.approx(0.0)
    assert choice_commission == pytest.approx(0.0)


def test_marketplace_commission_with_different_values() -> None:
    result = calculate_marketplace_commission(
        uber_revenue=12,
        wolt_revenue=2,
        glovo_revenue=30,
        pyszne_revenue=50,
    )

    assert result == pytest.approx(38.2)


def test_daily_result_can_be_negative() -> None:
    result = calculate_daily_result(
        gross_revenue=100,
        daily_costs=200,
        marketplace_commission=50,
        terminal_commission=10,
        choice_commission=5,
    )

    assert result == pytest.approx(-165.0)