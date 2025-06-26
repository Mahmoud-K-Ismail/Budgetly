from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from models import get_db, User, Expense
from schemas import ExpenseCreate, Expense as ExpenseSchema

router = APIRouter()

@router.post("/", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
async def create_expense(expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense record
    """
    # Verify user exists
    user = db.query(User).filter(User.id == expense_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create expense
    expense = Expense(
        user_id=expense_data.user_id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        expense_date=expense_data.expense_date
    )
    
    db.add(expense)
    db.commit()
    db.refresh(expense)
    
    return expense

@router.get("/", response_model=List[ExpenseSchema])
async def get_expenses(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    limit: int = Query(100, le=1000, description="Maximum number of expenses to return"),
    offset: int = Query(0, ge=0, description="Number of expenses to skip"),
    db: Session = Depends(get_db)
):
    """
    Get expenses with optional filtering
    """
    query = db.query(Expense)
    
    # Apply filters
    if user_id is not None:
        query = query.filter(Expense.user_id == user_id)
    
    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))
    
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    
    # Apply pagination
    expenses = query.order_by(Expense.expense_date.desc()).offset(offset).limit(limit).all()
    
    return expenses

@router.get("/id/{expense_id}", response_model=ExpenseSchema)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    Get a specific expense by ID
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return expense

@router.put("/id/{expense_id}", response_model=ExpenseSchema)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing expense
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Verify user exists
    user = db.query(User).filter(User.id == expense_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update expense fields
    expense.user_id = expense_data.user_id
    expense.amount = expense_data.amount
    expense.category = expense_data.category
    expense.description = expense_data.description
    expense.expense_date = expense_data.expense_date
    
    db.commit()
    db.refresh(expense)
    
    return expense

@router.delete("/id/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    Delete an expense
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
    
    return None

@router.get("/user/{user_id}/recent", response_model=List[ExpenseSchema])
async def get_recent_expenses(
    user_id: int,
    limit: int = Query(5, le=50, description="Number of recent expenses to return"),
    db: Session = Depends(get_db)
):
    """
    Get recent expenses for a specific user
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .limit(limit)
        .all()
    )
    
    return expenses

@router.get("/user/{user_id}/category/{category}", response_model=List[ExpenseSchema])
async def get_expenses_by_category(
    user_id: int,
    category: str,
    db: Session = Depends(get_db)
):
    """
    Get all expenses for a specific user and category
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id, Expense.category.ilike(f"%{category}%"))
        .order_by(Expense.expense_date.desc())
        .all()
    )
    
    return expenses

@router.post("/expenses", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
async def create_expense_explicit(expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense record (explicit /expenses path)
    """
    user = db.query(User).filter(User.id == expense_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    expense = Expense(
        user_id=expense_data.user_id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        expense_date=expense_data.expense_date
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/expenses", response_model=List[ExpenseSchema])
async def get_expenses_explicit(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    limit: int = Query(100, le=1000, description="Maximum number of expenses to return"),
    offset: int = Query(0, ge=0, description="Number of expenses to skip"),
    db: Session = Depends(get_db)
):
    """
    Get expenses with optional filtering (explicit /expenses path)
    """
    query = db.query(Expense)
    if user_id is not None:
        query = query.filter(Expense.user_id == user_id)
    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    expenses = query.order_by(Expense.expense_date.desc()).offset(offset).limit(limit).all()
    return expenses 