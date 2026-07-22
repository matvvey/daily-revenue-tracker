from calculations import (
    calculate_choice_commission,
    calculate_daily_result,
    calculate_marketplace_commission,
    calculate_terminal_commission,
)

def calculate_report(
    gross_revenue: float,
    daily_costs: float,
    uber_revenue: float,
    wolt_revenue: float,
    glovo_revenue: float,
    pyszne_revenue: float,
    terminal_revenue: float,
    choice_online_revenue: float,
) -> dict[str, float]:
    marketplace_revenue = (
        uber_revenue
        + wolt_revenue
        + glovo_revenue
        + pyszne_revenue
    )

    if marketplace_revenue > gross_revenue:
        raise ValueError("Suma sprzedaży marketplace jest większa niż obrót z kasy fiskalnej.")

    marketplace_commission = calculate_marketplace_commission(
        uber_revenue=uber_revenue,
        wolt_revenue=wolt_revenue,
        glovo_revenue=glovo_revenue,
        pyszne_revenue=pyszne_revenue,
    )

    terminal_commission = calculate_terminal_commission(
        terminal_revenue=terminal_revenue,
    )

    choice_commission = calculate_choice_commission(
        choice_online_revenue=choice_online_revenue,
    )

    daily_result = calculate_daily_result(
        gross_revenue=gross_revenue,
        daily_costs=daily_costs,
        marketplace_commission=marketplace_commission,
        terminal_commission=terminal_commission,
        choice_commission=choice_commission,
    )

    return {
        "marketplace_commission": marketplace_commission,
        "terminal_commission": terminal_commission,
        "choice_commission": choice_commission,
        "daily_result": daily_result,
    }