from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict
import io
from datetime import date, datetime

from models import get_db, User, Expense
from schemas import BudgetSummary, Recommendation
from utils.calculations import calculate_budget_summary, get_expense_statistics
from utils.recommendations import generate_recommendations, get_spending_insights

router = APIRouter()

@router.get("/summary/{user_id}", response_model=BudgetSummary)
async def get_budget_summary(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive budget summary for a user
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's expenses
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    # Calculate budget summary
    summary_data = calculate_budget_summary(user, expenses)
    
    return BudgetSummary(**summary_data)

@router.get("/recommendations/{user_id}", response_model=List[Recommendation])
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    Get personalized financial recommendations for a user
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's expenses
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    # Generate recommendations
    recommendations = generate_recommendations(user, expenses)
    
    return [Recommendation(**rec) for rec in recommendations]

@router.get("/insights/{user_id}")
async def get_spending_insights_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Get detailed spending insights and analysis
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's expenses
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    # Get insights
    insights = get_spending_insights(user, expenses)
    
    return {
        "user_id": user_id,
        "insights": insights["insights"],
        "patterns": insights["patterns"],
        "suggestions": insights["suggestions"]
    }

@router.get("/report/{user_id}")
async def get_expense_report(
    user_id: int,
    format: str = "json",
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """
    Get expense report for a user in JSON or CSV format
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Build query
    query = db.query(Expense).filter(Expense.user_id == user_id)
    
    # Apply date filters
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    
    # Get expenses
    expenses = query.order_by(Expense.expense_date.desc()).all()
    
    if format.lower() == "csv":
        # Create CSV report without pandas
        if not expenses:
            # Return empty CSV
            csv_content = "Date,Category,Description,Amount\n"
            return StreamingResponse(
                io.StringIO(csv_content),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=expenses_{user_id}.csv"}
            )
        
        # Create CSV content manually
        csv_lines = ["Date,Category,Description,Amount"]
        for expense in expenses:
            description = expense.description or ""
            # Escape quotes in description
            description = description.replace('"', '""')
            csv_lines.append(f'"{expense.expense_date}","{expense.category}","{description}",{expense.amount}')
        
        csv_content = "\n".join(csv_lines)
        
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=expenses_{user_id}.csv"}
        )
    
    else:
        # Return JSON report
        total_amount = sum(expense.amount for expense in expenses)
        
        return {
            "user_id": user_id,
            "total_expenses": len(expenses),
            "total_amount": total_amount,
            "period_start": start_date or user.budget_cycle_start,
            "period_end": end_date or date.today(),
            "expenses": [
                {
                    "id": expense.id,
                    "date": expense.expense_date,
                    "category": expense.category,
                    "description": expense.description,
                    "amount": expense.amount
                }
                for expense in expenses
            ]
        }

@router.get("/statistics/{user_id}")
async def get_expense_statistics_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Get detailed expense statistics for a user
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's expenses
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    # Get statistics
    stats = get_expense_statistics(expenses)
    
    return {
        "user_id": user_id,
        "statistics": stats
    }

@router.get("/dashboard/{user_id}")
async def get_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard data for a user
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's expenses
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    # Calculate all data
    budget_summary = calculate_budget_summary(user, expenses)
    recommendations = generate_recommendations(user, expenses)
    insights = get_spending_insights(user, expenses)
    statistics = get_expense_statistics(expenses)
    
    # Get recent expenses
    recent_expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .limit(5)
        .all()
    )
    
    return {
        "user": {
            "id": user.id,
            "stipend": user.stipend,
            "savings_goal": user.savings_goal,
            "budget_cycle_start": user.budget_cycle_start
        },
        "budget_summary": budget_summary,
        "recommendations": recommendations[:3],  # Top 3 recommendations
        "insights": insights,
        "statistics": statistics,
        "recent_expenses": [
            {
                "id": expense.id,
                "date": expense.expense_date,
                "category": expense.category,
                "description": expense.description,
                "amount": expense.amount
            }
            for expense in recent_expenses
        ]
    } 