UBER_RATE = 0.20
WOLT_RATE = 0.40
GLOVO_RATE = 0.50
PYSZNE_RATE = 0.40
TERMINAL_RATE = 0.02
CHOICE_ONLINE_RATE = 0.02


# Calculate total marketplace commissions
def calculate_marketplace_commission(
    uber_revenue: float,
    wolt_revenue: float,
    glovo_revenue: float,
    pyszne_revenue: float,
) -> float:
    return (
        uber_revenue * UBER_RATE
        + wolt_revenue * WOLT_RATE
        + glovo_revenue * GLOVO_RATE
        + pyszne_revenue * PYSZNE_RATE
    )


# Calculate terminal payment commission
def calculate_terminal_commission(
    terminal_revenue: float,
) -> float:
    return terminal_revenue * TERMINAL_RATE


# Calculate Choice Online payment commission
def calculate_choice_commission(
    choice_online_revenue: float,
) -> float:
    return choice_online_revenue * CHOICE_ONLINE_RATE


# Calculate daily result after costs and commissions
def calculate_daily_result(
    gross_revenue: float,
    daily_costs: float,
    marketplace_commission: float,
    terminal_commission: float,
    choice_commission: float,
) -> float:
    return (
        gross_revenue
        - daily_costs
        - marketplace_commission
        - terminal_commission
        - choice_commission
    )