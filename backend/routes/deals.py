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
    
    # Check if all deals have vague pricing (indicating the item might be too general)
    vague_price_count = sum(1 for deal in deals if isinstance(deal.get('price'), str) and 'varies' in deal.get('price', '').lower())
    
    # If most deals have vague pricing, suggest being more specific
    if vague_price_count >= len(deals) * 0.7:  # 70% or more have vague pricing
        # Add a helpful suggestion as the first deal
        suggestion_deal = {
            "merchant": "💡 Suggestion",
            "item_name": f"Be more specific about '{purchase.item_name}'",
            "price": "Try adding brand, model, size, or other details to get better price estimates",
            "url": "https://www.google.com/search?q=how+to+write+specific+product+descriptions"
        }
        deals = [suggestion_deal] + deals
    
    return deals 