from datetime import date
import streamlit as st
from costs_manager.models import CostCategory, FixedCost
from costs_manager.repository import FixedCostRepository
from costs_manager.service import FixedCostService

MONTH_NAMES = {
        1: "Styczeń",
        2: "Luty",
        3: "Marzec",
        4: "Kwiecień",
        5: "Maj",
        6: "Czerwiec",
        7: "Lipiec",
        8: "Sierpień",
        9: "Wrzesień",
        10: "Październik",
        11: "Listopad",
        12: "Grudzień",
    }

def _get_next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1

    return year, month + 1

def _format_cost_option(cost: FixedCost) -> str:
    return (
        f"{cost.name} - "
        f"{cost.amount:.2f} zł - "
        f"{cost.category.value}"
    )



# Manager fixed cost tables
def render_fixed_costs_manager(repository: FixedCostRepository) -> None:
    st.header("Koszty stałe")

    current_date = date.today()
    
    month_column, year_column = st.columns(2)

    with month_column:
        month = st.selectbox(
            "Miesiąc", 
            options=list(MONTH_NAMES), 
            index=current_date.month - 1, 
            format_func=lambda value:MONTH_NAMES[value],
            key="fixed_costs_month")

    with year_column:
        year = st.number_input(
            "Rok",
            min_value=2000,
            max_value=2100,
            value=current_date.year,
            step=1,
            key="fixed_costs_year"
        )


    repository.initialize_table()

    _render_add_fixed_cost_form(repository=repository, year=year, month=month)

    costs = repository.get_by_month(year=year, month=month)

    _render_fixed_costs_summary(costs=costs, year=year, month=month)

    _render_fixed_costs_table(costs=costs, year=year, month=month)

    _render_edit_fixed_cost_form(repository=repository, costs=costs)

    _render_delete_fixed_cost_form(repository=repository, costs=costs)

    _render_copy_fixed_costs_form(repository=repository, source_year=year, source_month=month)


def _render_add_fixed_cost_form(repository:FixedCostRepository, year: int, month: int) -> None:
    with st.expander("Dodaj koszt stały"):
        with st.form("add_fixed_cost_form"):
            name = st.text_input("Nazwa kosztu")

            amount = st.number_input("Kwota", min_value=0.0, step=10.0)
            category = st.selectbox("Kategoria", options=list(CostCategory), format_func=lambda item: item.value)
            notes = st.text_area("Notatki")
            submitted = st.form_submit_button("Dodaj koszt")

            if submitted:
                try:
                    cost = FixedCost(name=name, amount=amount, category=category, notes=notes or None, year=year, month=month)
                    repository.add(cost)

                    st.session_state["success_message"] = ("Koszt stały został dodany")
                    st.rerun()

                except ValueError as error:
                    st.error(str(error))

# Summary fixed cost table
def _render_fixed_costs_summary(costs: list[FixedCost], year: int, month: int) -> None:
    total = FixedCostService.calculate_total(costs)

    days_in_month = FixedCostService.get_days_in_month(year, month)
    daily_average = FixedCostService.calculate_daily_average(costs, year, month)

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric("Łączne koszty stałe", f"{total:.2f} zł")
    column_2.metric("Liczba dni", days_in_month)
    column_3.metric("Średni koszt dzienny", f"{daily_average:.2f} zł")


# Render fixed cost table
def _render_fixed_costs_table(costs: list[FixedCost], year: int, month: int) -> None:
    st.subheader("Lista kosztów")

    if not costs:
        st.info("Brak kosztów stałych dla wybranego miesiąca")
        return

    days_in_month = FixedCostService.get_days_in_month(year=year, month=month)

    costs_data = [
        {
            "Nazwa": cost.name,
            "Kategoria": cost.category.value,
            "Suma": cost.amount,
            "Średnio dziennie": cost.amount / days_in_month,
            "Notatki": cost.notes or ""
        }
        for cost in costs
    ]

    st.dataframe(
        costs_data, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Suma":st.column_config.NumberColumn(format="%.2f zł"),
            "Średnio dziennie": st.column_config.NumberColumn(format="%.2f zł")
        }
    )


# Edit fixed cost table
def _render_edit_fixed_cost_form(repository: FixedCostRepository, costs: list[FixedCost]) -> None:
    if not costs:
        return

    with st.expander("Edytuj koszt"):
        selected_cost = st.selectbox(
            "Wybierz koszt do edycji",
            options=costs,
            format_func=_format_cost_option,
            key="fixed_cost_to_edit"
        )

        with st.form("edit_fixed_cost_form"):
            edited_name = st.text_input("Nazwa kosztu", value=selected_cost.name)

            edited_amount = st.number_input("Kwota", value=float(selected_cost.amount), step=10.0)

            categories = list(CostCategory)

            selected_category_index = categories.index(selected_cost.category)

            edited_category = st.selectbox(
                "Kategoria", 
                options=categories, 
                index=selected_category_index, 
                format_func=lambda category: category.value
            )

            edited_notes = st.text_area("Notatki", value=selected_cost.notes or "")

            submitted = st.form_submit_button("Zapisz zmiany")
        if submitted:
            try:
                updated_cost = FixedCost(
                    id=selected_cost.id,
                    year=selected_cost.year,
                    month=selected_cost.month,
                    name=edited_name,
                    amount=edited_amount,
                    category=edited_category,
                    notes=edited_notes or None, 
                )

                repository.update(updated_cost)

                st.session_state["success_message"] = "Koszt został zaktualizowany"
                st.rerun()

            except ValueError as error:
                st.error(str(error))



# Delete fixed cost table

def _render_delete_fixed_cost_form(repository: FixedCostRepository, costs: list[FixedCost]) -> None:
    if not costs:
        return

    with st.expander("Usuń koszt"):
        with st.form("delete_fixed_cost_form"):
            selected_cost = st.selectbox(
                "Wybierz koszt do usunięcia",
                options=costs,
                format_func=_format_cost_option,
                key="fixed_cost_to_delete"
            )

            confirmation = st.checkbox("Potwierdzam usunięcie kosztu")

            submitted = st.form_submit_button("Usuń koszt")

            if submitted:
                if not confirmation:
                    st.warning("Potwierdź usunięcie kosztu")
                    return

                if selected_cost.id is None:
                    st.error("Nie można usunąć kosztu bez ID")
                    return

                try:
                    repository.delete(selected_cost.id)

                    st.session_state["success_message"] = "Koszt został usunięty."
                    st.rerun()

                except ValueError as error:
                    st.error(str(error))


def _render_copy_fixed_costs_form(repository: FixedCostRepository, source_year: int, source_month: int) -> None:
    default_target_year, default_target_month = _get_next_month(year=source_year, month=source_month)

    with st.expander("Kopiuj koszty do innego miesiąca"):
        st.write(
            "Miesiąc źródłowy: "
            f"{MONTH_NAMES[source_month]} {source_year}"
        )

        target_month_column, target_year_column = st.columns(2)

        with target_month_column:
            target_month = st.selectbox(
                "Miesiąc docelowy",
                options=list(MONTH_NAMES),
                index=default_target_month - 1,
                format_func=lambda value: MONTH_NAMES[value],
                key="fixed_costs_copy_target_month",
            )

        with target_year_column:
            target_year = st.number_input(
                "Rok docelowy",
                min_value=2000,
                max_value=2100,
                value=default_target_year,
                step=1,
                key="fixed_costs_copy_target_year",
            )

        confirmation = st.checkbox("Potwierdzam skopiowanie kosztów", key="fixed_costs_copy_confirmation")

        copy_button = st.button("Kopiuj koszty", key="copy_fixed_costs_button")

        if copy_button:
            if not confirmation:
                st.warning("Potwierdzam skopiowanie kosztów")
                return

            try:
                copied_count = repository.copy_to_month(
                    source_year=source_year, 
                    source_month=source_month, 
                    target_year=int(target_year),
                    target_month=target_month
                )

                st.session_state["success_message"] = (f"Skopiowano {copied_count} kosztów.")
                st.rerun()

            except ValueError as error:
                st.error(str(error))