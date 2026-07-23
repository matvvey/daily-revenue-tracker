import calendar
from costs_manager.models import FixedCost

class FixedCostService:
    @staticmethod
    def get_days_in_month(year: int, month: int) -> int:
        if year < 2000:
            raise ValueError("Nieprawidłowy rok.")

        if not 1 <= month <= 12:
            raise ValueError("Miesiąc musi być w zakresie 1-12.")

        return calendar.monthrange(year, month)[1]

    @staticmethod
    def calculate_total(costs: list[FixedCost]) -> float:
        return sum(cost.amount for cost in costs)

    @classmethod
    def calculate_daily_average(cls, costs: list[FixedCost], year: int, month: int) -> float:
        total = cls.calculate_total(costs)

        days_in_month = cls.get_days_in_month(year, month)

        return total / days_in_month