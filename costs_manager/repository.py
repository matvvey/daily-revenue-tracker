import sqlite3
from costs_manager.models import CostCategory, FixedCost
from pathlib import Path
from database import DATABASE_PATH, get_connection

class FixedCostRepository:
    def __init__(self, database_path: Path=DATABASE_PATH) -> None:
        self.database_path = database_path


    def initialize_table(self) -> None:
        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS fixed_costs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    
                    CHECK (year >= 2000),
                    CHECK (month BETWEEN 1 AND 12),
                    CHECK (amount > 0)
                )
                """,
            )

    def add(self, cost: FixedCost) -> FixedCost:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO fixed_costs (
                    year, month, name, amount, category, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    cost.year, 
                    cost.month, 
                    cost.name, 
                    cost.amount, 
                    cost.category, 
                    cost.notes
                ),
            )

            cost.id = cursor.lastrowid

        return cost

    def get_by_month(self, year: int, month: int) -> list[FixedCost]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, year, month, name, amount, category, notes FROM fixed_costs
                WHERE year = ? and month = ?
                ORDER BY category, name
                """, (year, month),
            ).fetchall()

        return [
            self._row_to_fixed_cost(row)
            for row in rows
            ]

    def update(self, cost: FixedCost) -> None:
        if cost.id is None:
            raise ValueError("Nie można zaktualizować kosztu bez ID.")

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                UPDATE fixed_costs
                SET year = ?, month = ?, name = ?, amount = ?, category = ?, notes = ?
                WHERE id = ?
                """,
                (
                    cost.year, 
                    cost.month, 
                    cost.name, 
                    cost.amount,
                    cost.category.value, 
                    cost.notes, 
                    cost.id
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError("Nie znaleziono kosztu do aktualizacji.")

    def delete(self, cost_id: int) -> None:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                DELETE FROM fixed_costs
                WHERE id = ?
                """,
                (cost_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Nie znaleziono kosztu do usunięcia.")

    @staticmethod
    def _row_to_fixed_cost(row: sqlite3.Row) -> FixedCost:
        return FixedCost(
            id=row["id"],
            year=row["year"],
            month=row["month"],
            name=row["name"],
            amount=row["amount"],
            category=CostCategory(row["category"]),
            notes=row["notes"],
        )