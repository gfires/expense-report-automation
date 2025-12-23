from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class ReportItem:
    description: str
    activity: str
    date: date
    price: float
    vendor: str
    receipts: List[str]
    flyer: str

@dataclass
class ExpectedExpense:
    date: date
    vendor: str
    price: float
