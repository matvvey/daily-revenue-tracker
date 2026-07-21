import streamlit as st
import sqlite3
from datetime import date
from database import (
    initialize_database,
    save_daily_report,
    get_daily_reports,
    update_daily_report,
    delete_daily_report,
)
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

if "success_message" in st.session_state:
    st.success(st.session_state.pop("success_message"))

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
            daily_result=daily_result,
        )

        st.success("Raport został zapisany.")

    except sqlite3.IntegrityError:
        st.error(
            "Raport dla wybranej daty już istnieje."
        )

# Reports history
st.divider()
st.subheader("Historia raportów")

reports = get_daily_reports()

if not reports:
    st.info("Brak zapisanych raportów.")
else:
    reports_data = [
        {
            "Data": report["report_date"],
            "Obrót brutto": report["gross_revenue"],
            "Koszty dzienne": report["daily_costs"],
            "Prowizje marketplace": report["marketplace_commission"],
            "Prowizja terminala": report["terminal_commission"],
            "Prowizja Choice Online": report["choice_commission"],
            "Wynik dnia": report["daily_result"],
        }
        for report in reports
    ]

    st.dataframe(
        reports_data,
        use_container_width=True,
        hide_index=True,
    )

# Modify reports

st.subheader("Zarządzanie raportami")

if reports:
    reports_by_id = {
        report["id"]: report
        for report in reports
    }

    selected_report_id = st.selectbox(
        "Wybierz raport",
        options=list(reports_by_id.keys()),
        format_func=lambda report_id: reports_by_id[report_id]["report_date"],
    )

    selected_report = reports_by_id[selected_report_id]

    # Form to modify report
    with st.expander("Edytuj raport"):
        with st.form("edit_report_form"):
            edited_report_date = st.date_input(
                "Data raportu",
                value=date.fromisoformat(
                    selected_report["report_date"]
                ),
            )

            edited_gross_revenue = st.number_input(
                "Obrót z kasy fiskalnej",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["gross_revenue"]),
            )

            edited_daily_costs = st.number_input(
                "Koszty dzienne",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["daily_costs"]),
            )

            st.write("Kanały sprzedaży")

            edited_uber_revenue = st.number_input(
                "Uber Eats",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["uber_revenue"]),
            )

            edited_wolt_revenue = st.number_input(
                "Wolt",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["wolt_revenue"]),
            )

            edited_glovo_revenue = st.number_input(
                "Glovo",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["glovo_revenue"]),
            )

            edited_pyszne_revenue = st.number_input(
                "Pyszne",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["pyszne_revenue"]),
            )

            edited_terminal_revenue = st.number_input(
                "Terminal",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["terminal_revenue"]),
            )


            edited_choice_online_revenue = st.number_input(
                "Choice Online",
                min_value=0.0,
                step=10.0,
                value=float(selected_report["choice_online_revenue"]),
            )

            update_submitted = st.form_submit_button("Zapisz zmiany")

    if update_submitted:
        edited_marketplace_revenue = (
            edited_uber_revenue
            + edited_wolt_revenue
            + edited_glovo_revenue
            + edited_pyszne_revenue
        )
        if edited_marketplace_revenue > edited_gross_revenue:
            st.error("Suma sprzedaży marketplace jest większa niż obrót kasy fiskalnej.")
        else:
            edited_marketplace_commission = (
                calculate_marketplace_commission(
                    uber_revenue=edited_uber_revenue,
                    wolt_revenue=edited_wolt_revenue,
                    glovo_revenue=edited_glovo_revenue,
                    pyszne_revenue=edited_pyszne_revenue,
                )
            )
            edited_terminal_commission = (
                calculate_terminal_commission(terminal_revenue=edited_terminal_revenue)
            )

            edited_choice_commission = (
                calculate_choice_commission(choice_online_revenue=edited_choice_online_revenue)
            )

            edited_daily_result = calculate_daily_result(
                    gross_revenue=edited_gross_revenue,
                    daily_costs=edited_daily_costs,
                    marketplace_commission=edited_marketplace_commission,
                    terminal_commission=edited_terminal_commission,
                    choice_commission=edited_choice_commission,
                )
            
            try:
                update_daily_report(
                    report_id=selected_report_id,
                    report_date=edited_report_date,
                    gross_revenue=edited_gross_revenue,
                    daily_costs=edited_daily_costs,
                    uber_revenue=edited_uber_revenue,
                    wolt_revenue=edited_wolt_revenue,
                    glovo_revenue=edited_glovo_revenue,
                    pyszne_revenue=edited_pyszne_revenue,
                    terminal_revenue=edited_terminal_revenue,
                    choice_online_revenue=edited_choice_online_revenue,
                    marketplace_commission=edited_marketplace_commission,
                    terminal_commission=edited_terminal_commission,
                    choice_commission=edited_choice_commission,
                    daily_result=edited_daily_result,
                )

                st.session_state["success_message"] = ("Raport został zaktualizowany.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Raport dla wybranej daty już istnieje.")
        

    # Delete report
    with st.expander("Usuń raport"):
        st.warning("Usunięcie raportu jest nieodwracalne!")

        confirm_delete = st.checkbox("Potwierdzam usunięcie raportu", key=f"confirm_delete_{selected_report_id}")
        if st.button("Usuń raport", disabled=not confirm_delete, type="primary"):
            delete_daily_report(selected_report_id)

            st.session_state["success_message"] = "Raport został usunięty."
            st.rerun()