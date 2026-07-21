import sqlite3
from pathlib import Path
from datetime import date

DATABASE_PATH = Path("data") / "daily_revenue.db"

def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT NOT NULL UNIQUE,
            
            gross_revenue REAL NOT NULL,
            daily_costs REAL NOT NULL,
            
            uber_revenue REAL NOT NULL,
            wolt_revenue REAL NOT NULL,
            glovo_revenue REAL NOT NULL,
            pyszne_revenue REAL NOT NULL,
            
            terminal_revenue REAL NOT NULL,
            choice_online_revenue REAL NOT NULL,
            
            marketplace_commission REAL NOT NULL,
            terminal_commission REAL NOT NULL,
            choice_commission REAL NOT NULL,

            daily_result REAL NOT NULL,

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_daily_report(
    report_date: date,
    gross_revenue: float,
    daily_costs: float,
    uber_revenue: float,
    wolt_revenue: float,
    glovo_revenue: float,
    pyszne_revenue: float,
    terminal_revenue: float,
    choice_online_revenue: float,
    marketplace_commission: float,
    terminal_commission: float,
    choice_commission: float,
    daily_result: float,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO daily_reports (
                report_date,
                gross_revenue,
                daily_costs,
                uber_revenue,
                wolt_revenue,
                glovo_revenue,
                pyszne_revenue,
                terminal_revenue,
                choice_online_revenue,
                marketplace_commission,
                terminal_commission,
                choice_commission,
                daily_result
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_date.isoformat(),
                gross_revenue,
                daily_costs,
                uber_revenue,
                wolt_revenue,
                glovo_revenue,
                pyszne_revenue,
                terminal_revenue,
                choice_online_revenue,
                marketplace_commission,
                terminal_commission,
                choice_commission,
                daily_result,
            ),
        )