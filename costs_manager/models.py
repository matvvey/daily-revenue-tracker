from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

class CostCategory(StrEnum):
    PRODUCTS = "Produkty"
    PACKAGING = "Opakowania"
    CLEANING = "Chemia i środki czystości"
    EQUIPMENT = "Sprzęt"
    REPAIRS = "Naprawy"
    MARKETING = "Marketing"
    ADMINISTRATION = "Administracja"
    UTILITIES = "Media"
    SUBSCRIPTIONS = "Subskrypcje"
    RENT = "Lokal"
    OTHER = "Inne"

@dataclass
class Cost:
    name: str
    amount: float
    category: CostCategory
    notes: str | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Nazwa kosztu nie może być pusta.")
        if self.amount < 0:
            raise ValueError("Kwota kosztu nie może być ujemna.")

@dataclass
class FixedCost(Cost):
    year: int = 0
    month: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.year < 2000:
            raise ValueError("Nieprawidłowy rok.")

        if not 1 <= self.month <= 12:
            raise ValueError("Miesiąc musi być w zakresie 1-12.")

@dataclass
class DailyCost(Cost):
    cost_date: date = field(default_factory=date.today)
    vendor: str | None = None
    document_number: str | None = None