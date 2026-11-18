from datetime import date
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    spent_on: Mapped[date]
    note: Mapped[str | None] = mapped_column(String(255))
    is_income: Mapped[bool] = mapped_column(default=False)
