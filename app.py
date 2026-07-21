import streamlit as st

from calculations import (
    calculate_choice_commission,
    calculate_marketplace_commission,
    calculate_net_revenue,
    calculate_terminal_commission,
)

st.set_page_config(
    page_title="Daily Revenue Tracker",
    page_icon="📊"
)

st.title("Daily Revenue Tracker")
st.write("Wprowadź dane z raportu dziennego.")

gross_revenue = st.number_input(
    "Obrót z kasy fiskalnej",
    min_value=0.0,
    step=10.0,
)

daily_costs = st.number_input(
    "Koszty dzienne",
    min_value=0.0,
    step=10.0,
)

st.subheader("Kanały sprzedaży")

uber_revenue = st.number_input(
    "Uber Eats",
    min_value=0.0,
    step=10.0,
)

wolt_revenue = st.number_input(
    "Wolt",
    min_value=0.0,
    step=10.0,
)

glovo_revenue = st.number_input(
    "Glovo",
    min_value=0.0,
    step=10.0,
)

pyszne_revenue = st.number_input(
    "Pyszne",
    min_value=0.0,
    step=10.0,
)

terminal_revenue = st.number_input(
    "Terminal",
    min_value=0.0,
    step=10.0,
)

choice_online_revenue = st.number_input(
    "Choice Online",
    min_value=0.0,
    step=10.0,
)

if st.button("Oblicz wynik dnia"):
    marketplace_commission = calculate_marketplace_commission(
        uber_revenue=uber_revenue,
        wolt_revenue=wolt_revenue,
        glovo_revenue=glovo_revenue,
        pyszne_revenue=pyszne_revenue,
    )

    terminal_commision = calculate_terminal_commission(
        terminal_revenue=terminal_revenue,
    )

    choice_commision = calculate_choice_commission(
        choice_online_revenue=choice_online_revenue,
    )

    net_revenue = calculate_net_revenue(
        gross_revenue=gross_revenue,
        daily_costs=daily_costs,
        marketplace_commission=marketplace_commission,
        terminal_commission=terminal_commision,
        choice_commission=choice_commision,
    )

    st.subheader("Podsumowanie")

    st.metric(
        "Obrót brutto",
        f"{gross_revenue:.2f} zł",
    )

    st.metric(
        "Prowizje marketplace",
        f"{marketplace_commission:.2f} zł",
    )

    st.metric(
        "Prowizja z terminału",
        f"{terminal_commision:.2f} zł",
    )

    st.metric(
        "Prowizja z płatności Choice Online",
        f"{choice_commision:.2f} zł",
    )

    st.metric(
        "Wynik po kosztach i prowizjach",
        f"{net_revenue:.2f} zł",
    )

# Checking the logic of marketplaces revenue data (the markeplaces revenue must not be greater than total revenue)
reported_channels_revenue = (
    uber_revenue
    + wolt_revenue
    + glovo_revenue
    + pyszne_revenue
)

if reported_channels_revenue > gross_revenue:
    st.error(
        "Suma sprzedaży marketplace jest większa niż obrót z kasy fiskalnej. Sprawdź poprawność danych."
    )
    st.stop()