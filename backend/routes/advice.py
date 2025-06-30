from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import get_db, User, Expense, PlannedPurchase
from utils.ai_advisor import generate_advice

router = APIRouter()


@router.get("/advice/{user_id}")
async def get_ai_advice(user_id: int, db: Session = Depends(get_db)):
    """Return AI-generated budgeting advice for the user, including cuts and planned purchase verdicts."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    planned = db.query(PlannedPurchase).filter(PlannedPurchase.user_id == user_id).all()

    advice = generate_advice(user, expenses, planned)

    return advice 