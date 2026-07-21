import streamlit as st
import sqlite3
from database import initialize_database, save_daily_report
from calculations import (
    calculate_choice_commission,
    calculate_marketplace_commission,
    calculate_daily_result,
    calculate_terminal_commission,
)


st.set_page_config(
    page_title="Daily Revenue Tracker",
    page_icon="📊",
)

initialize_database()

st.title("Daily Revenue Tracker")
st.write("Wprowadź dane z raportu dziennego.")

report_date = st.date_input(
    "Data raportu",
)

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
    "Pyszne.pl",
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

if st.button("Oblicz i zapisz raport"):

    # Calculate data 
    reported_marketplace_revenue = (
        uber_revenue
        + wolt_revenue
        + glovo_revenue
        + pyszne_revenue
    )

    if reported_marketplace_revenue > gross_revenue:
        st.error(
            "Suma sprzedaży marketplace jest większa niż obrót z kasy fiskalnej. Sprawdź poprawność danych."
        )
        st.stop()

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
        "Prowizja terminal",
        f"{terminal_commission:.2f} zł",
    )

    st.metric(
        "Prowizja płatności Choice Online",
        f"{choice_commission:.2f} zł",
    )

    st.metric(
        "Wynik po kosztach i prowizjach",
        f"{daily_result:.2f} zł",
    )

    # Save report to DB
    try:
        save_daily_report(
            report_date=report_date,
            gross_revenue=gross_revenue,
            daily_costs=daily_costs,
            uber_revenue=uber_revenue,
            wolt_revenue=wolt_revenue,
            glovo_revenue=glovo_revenue,
            pyszne_revenue=pyszne_revenue,
            terminal_revenue=terminal_revenue,
            choice_online_revenue=choice_online_revenue,
            marketplace_commission=marketplace_commission,
            terminal_commission=terminal_commission,
            choice_commission=choice_commission,
            daily_result=gross_revenue,
        )

        st.success("Raport został zapisany.")

    except sqlite3.IntegrityError:
        st.error(
            "Raport dla wybranej daty już istnieje."
        )