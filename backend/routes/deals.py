from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import get_db, PlannedPurchase
from utils.deal_finder import find_deals
from schemas import DealSuggestion

router = APIRouter()

@router.get("/deals/{purchase_id}", response_model=List[DealSuggestion])
async def get_deals(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(PlannedPurchase).filter(PlannedPurchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planned purchase not found")

    deals = find_deals(purchase.item_name)
    return deals 