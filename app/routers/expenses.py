from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_expense_or_404(expense_id: int, db: Session) -> Expense:
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("", response_model=list[ExpenseOut])
def list_expenses(
    category: str | None = None,
    is_income: bool | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Expense)
    if category is not None:
        query = query.where(Expense.category == category)
    if is_income is not None:
        query = query.where(Expense.is_income == is_income)
    if date_from is not None:
        query = query.where(Expense.spent_on >= date_from)
    if date_to is not None:
        query = query.where(Expense.spent_on <= date_to)
    query = query.order_by(Expense.spent_on.desc(), Expense.id.desc()).limit(limit).offset(offset)
    return db.scalars(query).all()


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return get_expense_or_404(expense_id, db)


@router.post("", response_model=ExpenseOut, status_code=201)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    expense = Expense(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.patch("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = get_expense_or_404(expense_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = get_expense_or_404(expense_id, db)
    db.delete(expense)
    db.commit()
    return Response(status_code=204)
