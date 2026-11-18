from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    spent_on: date
    note: str | None = Field(default=None, max_length=255)
    is_income: bool = False


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    spent_on: date | None = None
    note: str | None = Field(default=None, max_length=255)
    is_income: bool | None = None


class ExpenseOut(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
