from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from models import get_db, User
from schemas import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/user", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user profile with stipend, savings goal, and budget cycle start date
    """
    try:
        # Create new user
        db_user = User(
            stipend=user_data.stipend,
            savings_goal=user_data.savings_goal,
            budget_cycle_start=user_data.budget_cycle_start
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user profile by ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/users", response_model=List[UserSchema])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users (for development/testing purposes)
    """
    users = db.query(User).all()
    return users

@router.put("/user/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, 
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Update user profile
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        user.stipend = user_data.stipend
        user.savings_goal = user_data.savings_goal
        user.budget_cycle_start = user_data.budget_cycle_start
        
        db.commit()
        db.refresh(user)
        
        return user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user and all associated expenses
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        db.delete(user)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        ) 