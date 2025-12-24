from pydantic import BaseModel, Field
from typing import List


class ReconcileRequest(BaseModel):
    cardholder_name: str = Field(..., min_length=1, description="Name of cardholder to filter")
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Start date in YYYY-MM-DD format")
    expected_expenses: str = Field(..., description="Expected expenses text block (MM/DD/YY - Vendor - $Price)")

    class Config:
        json_schema_extra = {
            "example": {
                "cardholder_name": "Gavin Firestone (Treasurer)",
                "start_date": "2025-11-01",
                "expected_expenses": "11/1/25 - Trader Joe's - $25.25\n11/3/25 - Target - $9.99"
            }
        }


class ExpectedExpenseSchema(BaseModel):
    date: str
    vendor: str
    price: float

    @classmethod
    def from_dataclass(cls, exp):
        """Convert ExpectedExpense dataclass to Pydantic model"""
        return cls(
            date=exp.date.isoformat(),
            vendor=exp.vendor,
            price=exp.price
        )


class ReportItemSchema(BaseModel):
    description: str
    activity: str
    date: str
    price: float
    vendor: str
    receipts: List[str]
    flyer: str

    @classmethod
    def from_dataclass(cls, item):
        """Convert ReportItem dataclass to Pydantic model"""
        return cls(
            description=item.description,
            activity=item.activity,
            date=item.date.isoformat(),
            price=item.price,
            vendor=item.vendor,
            receipts=item.receipts,
            flyer=item.flyer
        )


class MatchedPair(BaseModel):
    expected: ExpectedExpenseSchema
    actual: ReportItemSchema


class ReconcileResponse(BaseModel):
    matched: List[MatchedPair]
    unmatched_expected: List[ExpectedExpenseSchema]
    unmatched_actual: List[ReportItemSchema]
