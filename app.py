import streamlit as st
import sqlite3
from report_service import calculate_report
from datetime import date
from database import (
    initialize_database,
    save_daily_report,
    get_daily_reports,
    update_daily_report,
    delete_daily_report,
)

# Page init
st.set_page_config(page_title="Daily Revenue Tracker", page_icon="📊")

initialize_database()

if "success_message" in st.session_state:
    st.success(st.session_state.pop("success_message"))

st.title("Daily Revenue Tracker")
st.write("Wprowadź dane z raportu dziennego.")

report_date = st.date_input("Data raportu")

gross_revenue = st.number_input("Obrót z kasy fiskalnej", min_value=0.0, step=10.0)

daily_costs = st.number_input("Koszty dzienne", min_value=0.0, step=10.0)

# Render fields
marketplace_fields = {
    "uber_revenue": "Uber Eats",
    "wolt_revenue": "Wolt",
    "glovo_revenue": "Glovo",
    "pyszne_revenue": "Pyszne",
}

payment_fields = {
    "terminal_revenue": "Terminal",
    "choice_online_revenue": "Choice Online"
}

def render_revenue_inputs(
        fields: dict[str, str],
        key_prefix: str,
        initial_values: dict[str, float] | None = None,
) -> dict[str, float]:
    values = {}
    initial_values = initial_values or {}

    for field_name, label in fields.items():
        values[field_name] = st.number_input(
            label=label,
            min_value=0.0,
            step=10.0,
            value=float(initial_values.get(field_name, 0.0)),
            key=f"{key_prefix}{field_name}",
        )
        
    return values

st.subheader("Kanały sprzedaży")

marketplace_revenues = render_revenue_inputs(
    marketplace_fields,
    key_prefix="create_",
)

st.subheader("Metody płatności")

payment_revenues = render_revenue_inputs(
    payment_fields,
    key_prefix="create_"
)

if st.button("Oblicz i zapisz raport"):

    # Calculate data
    try:
        result = calculate_report(
            gross_revenue=gross_revenue,
            daily_costs=daily_costs,
            uber_revenue=marketplace_revenues["uber_revenue"],
            wolt_revenue=marketplace_revenues["wolt_revenue"],
            glovo_revenue=marketplace_revenues["glovo_revenue"],
            pyszne_revenue=marketplace_revenues["pyszne_revenue"],
            terminal_revenue=payment_revenues["terminal_revenue"],
            choice_online_revenue=payment_revenues["choice_online_revenue"],
        )
    except ValueError as e:
        st.error(str(e))
        st.stop() 

    marketplace_commission = result["marketplace_commission"]

    terminal_commission = result["terminal_commission"]

    choice_commission = result["choice_commission"]

    daily_result = result["daily_result"]

    st.subheader("Podsumowanie")

    st.metric("Obrót brutto", f"{gross_revenue:.2f} zł")

    st.metric("Prowizje marketplace", f"{marketplace_commission:.2f} zł")

    st.metric("Prowizja terminal", f"{terminal_commission:.2f} zł")

    st.metric("Prowizja płatności Choice Online", f"{choice_commission:.2f} zł")

    st.metric("Wynik po kosztach i prowizjach", f"{daily_result:.2f} zł")

    # Save report to DB
    try:
        save_daily_report(
            report_date=report_date,
            gross_revenue=gross_revenue,
            daily_costs=daily_costs,
            uber_revenue=marketplace_revenues["uber_revenue"],
            wolt_revenue=marketplace_revenues["wolt_revenue"],
            glovo_revenue=marketplace_revenues["glovo_revenue"],
            pyszne_revenue=marketplace_revenues["pyszne_revenue"],
            terminal_revenue=payment_revenues["terminal_revenue"],
            choice_online_revenue=payment_revenues["choice_online_revenue"],
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
        "Wybierz raport do edycji",
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

            edited_marketplace_revenues = render_revenue_inputs(
                marketplace_fields,
                key_prefix=f"edit_{selected_report_id}_",
                initial_values={
                    "uber_revenue": selected_report["uber_revenue"],
                    "wolt_revenue": selected_report["wolt_revenue"],
                    "glovo_revenue": selected_report["glovo_revenue"],
                    "pyszne_revenue": selected_report["pyszne_revenue"],
                }
            )

            st.write("Metody płatności")

            edited_payment_revenues = render_revenue_inputs(
                fields=payment_fields,
                key_prefix=f"edit_{selected_report_id}_",
                initial_values={
                    "terminal_revenue": selected_report["terminal_revenue"],
                    "choice_online_revenue": selected_report["choice_online_revenue"]
                }
            )

            update_submitted = st.form_submit_button("Zapisz zmiany")

    if update_submitted:
        try:
            edited_result = calculate_report(
                gross_revenue=edited_gross_revenue,
                daily_costs=edited_daily_costs,
                uber_revenue=edited_marketplace_revenues[
                    "uber_revenue"
                ],
                wolt_revenue=edited_marketplace_revenues[
                    "wolt_revenue"
                ],
                glovo_revenue=edited_marketplace_revenues[
                    "glovo_revenue"
                ],
                pyszne_revenue=edited_marketplace_revenues[
                    "pyszne_revenue"
                ],
                terminal_revenue=edited_payment_revenues[
                    "terminal_revenue"
                ],
                choice_online_revenue=edited_payment_revenues[
                    "choice_online_revenue"
                ],
            )

        except ValueError as error:
            st.error(str(error))

        else:
            try:
                update_daily_report(
                    report_id=selected_report_id,
                    report_date=edited_report_date,
                    gross_revenue=edited_gross_revenue,
                    daily_costs=edited_daily_costs,
                    uber_revenue=edited_marketplace_revenues["uber_revenue"],
                    wolt_revenue=edited_marketplace_revenues["wolt_revenue"],
                    glovo_revenue=edited_marketplace_revenues["glovo_revenue"],
                    pyszne_revenue=edited_marketplace_revenues["pyszne_revenue"],
                    terminal_revenue=edited_payment_revenues["terminal_revenue"],
                    choice_online_revenue=edited_payment_revenues["choice_online_revenue"],
                    marketplace_commission=edited_result["marketplace_commission"],
                    terminal_commission=edited_result["terminal_commission"],
                    choice_commission=edited_result["choice_commission"],
                    daily_result=edited_result["daily_result"],
                )

                st.session_state["success_message"] = ("Raport został zaktualizowany.")
                st.rerun()

            except sqlite3.IntegrityError:
                st.error("Raport dla wybranej daty już istnieje.")
        

    # Delete report
    with st.expander("Usuń raport"):
        st.warning("Usunięcie raportu jest nieodwracalne!")

        with st.form(f"delete_report_form_{selected_report_id}"):
            confirm_delete = st.checkbox("Potwierdzam usunięcie raportu")

            delete_submitted = st.form_submit_button("Usuń raport", type="primary")

        if delete_submitted:
            if not confirm_delete:
                st.error("Potwierdź usunięcie raportu.")
            else:
                delete_daily_report(selected_report_id)

                st.session_state["success_message"] = ("Raport został usunięty.")
                st.rerun()