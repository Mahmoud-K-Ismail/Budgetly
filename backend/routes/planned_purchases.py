from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from models import get_db, User, PlannedPurchase
from schemas import PlannedPurchaseCreate, PlannedPurchase as PlannedPurchaseSchema

router = APIRouter()


@router.post("/planned-purchases", response_model=PlannedPurchaseSchema, status_code=status.HTTP_201_CREATED)
async def create_planned_purchase(purchase_data: PlannedPurchaseCreate, db: Session = Depends(get_db)):
    """Add a new planned purchase for a user"""
    user = db.query(User).filter(User.id == purchase_data.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    purchase = PlannedPurchase(
        user_id=purchase_data.user_id,
        item_name=purchase_data.item_name,
        expected_price=purchase_data.expected_price,
        priority=purchase_data.priority,
        desired_date=purchase_data.desired_date,
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


@router.get("/planned-purchases/{user_id}", response_model=List[PlannedPurchaseSchema])
async def list_planned_purchases(user_id: int, db: Session = Depends(get_db)):
    """List all planned purchases for a user"""
    purchases = db.query(PlannedPurchase).filter(PlannedPurchase.user_id == user_id).all()
    return purchases


@router.delete("/planned-purchases/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planned_purchase(purchase_id: int, db: Session = Depends(get_db)):
    """Delete a planned purchase"""
    purchase = db.query(PlannedPurchase).filter(PlannedPurchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planned purchase not found")
    db.delete(purchase)
    db.commit()
    return None 