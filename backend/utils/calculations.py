from datetime import date, datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from models import User, Expense

def calculate_budget_summary(user: User, expenses: List[Expense]) -> Dict[str, Any]:
    """
    Calculate comprehensive budget summary for a user
    
    Args:
        user: User object with stipend and savings goal
        expenses: List of user's expenses
    
    Returns:
        Dictionary with budget summary data
    """
    today = date.today()
    
    # Calculate days elapsed and remaining in budget cycle
    days_elapsed = (today - user.budget_cycle_start).days
    days_remaining = 30 - days_elapsed  # Assuming monthly cycle
    
    # Calculate total expenses
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Calculate remaining budget
    remaining_budget = user.stipend - total_expenses
    
    # Calculate daily limit
    daily_limit = remaining_budget / max(days_remaining, 1)
    
    # Group expenses by category
    expenses_by_category = {}
    for expense in expenses:
        category = expense.category
        if category not in expenses_by_category:
            expenses_by_category[category] = 0
        expenses_by_category[category] += expense.amount
    
    return {
        "stipend": user.stipend,
        "expenses_by_category": expenses_by_category,
        "savings_goal": user.savings_goal,
        "remaining_budget": remaining_budget,
        "daily_limit": daily_limit,
        "total_expenses": total_expenses,
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining
    }

def calculate_spending_trends(expenses: List[Expense]) -> Dict[str, Any]:
    """Return spending trend metrics expected by recommendations helpers."""
    if not expenses:
        return {
            "average_daily_spending": 0,
            "total_spending": 0,
            "expense_count": 0,
            "daily_spending": {}
        }
    total_spent = sum(e.amount for e in expenses)
    expense_count = len(expenses)
    # Aggregate by date
    daily_spending = {}
    for e in expenses:
        d = e.expense_date
        daily_spending[d] = daily_spending.get(d, 0) + e.amount
    average_daily = total_spent / len(daily_spending)
    return {
        "average_daily_spending": average_daily,
        "total_spending": total_spent,
        "expense_count": expense_count,
        "daily_spending": daily_spending
    }

def calculate_savings_progress(user: User, expenses: List[Expense]) -> Dict[str, Any]:
    """
    Calculate savings progress and projections
    
    Args:
        user: User object with savings goal
        expenses: List of user's expenses
    
    Returns:
        Dictionary with savings progress data
    """
    total_expenses = sum(expense.amount for expense in expenses)
    actual_savings = user.stipend - total_expenses
    savings_rate = (actual_savings / user.stipend) * 100 if user.stipend > 0 else 0
    
    # Project annual savings
    annual_savings = actual_savings * 12
    
    # Calculate if on track for savings goal
    monthly_savings_goal = user.savings_goal
    on_track = actual_savings >= monthly_savings_goal
    
    return {
        "actual_savings": actual_savings,
        "savings_rate": savings_rate,
        "annual_projection": annual_savings,
        "on_track_for_goal": on_track,
        "goal_shortfall": max(0, monthly_savings_goal - actual_savings),
        # Legacy keys for compatibility
        "on_track": on_track,
        "deficit": max(0, monthly_savings_goal - actual_savings)
    }

def get_expense_statistics(expenses: List[Expense]) -> Dict[str, Any]:
    """
    Calculate detailed expense statistics
    """
    if not expenses:
        return {
            "total_expenses": 0,
            "total_amount": 0,
            "average_amount": 0,
            "largest_expense": 0,
            "smallest_expense": 0,
            "category_breakdown": {},
            "monthly_trend": {},
            "daily_average": 0
        }
    
    # Basic statistics
    total_expenses = len(expenses)
    total_amount = sum(expense.amount for expense in expenses)
    amounts = [expense.amount for expense in expenses]
    average_amount = total_amount / total_expenses
    largest_expense = max(amounts)
    smallest_expense = min(amounts)
    
    # Category breakdown
    category_breakdown = {}
    for expense in expenses:
        category = expense.category
        if category not in category_breakdown:
            category_breakdown[category] = {"count": 0, "total": 0}
        category_breakdown[category]["count"] += 1
        category_breakdown[category]["total"] += expense.amount
    
    # Monthly trend
    monthly_trend = {}
    for expense in expenses:
        expense_date = expense.expense_date
        month_key = f"{expense_date.year}-{expense_date.month:02d}"
        if month_key not in monthly_trend:
            monthly_trend[month_key] = 0
        monthly_trend[month_key] += expense.amount
    
    # Daily average (last 30 days)
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_expenses = [exp for exp in expenses if exp.expense_date >= thirty_days_ago]
    daily_average = sum(exp.amount for exp in recent_expenses) / 30 if recent_expenses else 0
    
    return {
        "total_expenses": total_expenses,
        "total_amount": total_amount,
        "average_amount": average_amount,
        "largest_expense": largest_expense,
        "smallest_expense": smallest_expense,
        "category_breakdown": category_breakdown,
        "monthly_trend": monthly_trend,
        "daily_average": daily_average
    }

def get_spending_patterns(expenses: List[Expense]) -> Dict[str, Any]:
    """
    Analyze spending patterns and trends
    """
    if not expenses:
        return {
            "top_categories": [],
            "spending_trend": "stable",
            "peak_spending_day": None,
            "peak_spending_month": None
        }
    
    # Top spending categories
    category_totals = {}
    for expense in expenses:
        category = expense.category
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += expense.amount
    
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Spending by day of week
    day_spending = {i: 0 for i in range(7)}
    for expense in expenses:
        expense_date = expense.expense_date
        day_spending[expense_date.weekday()] += expense.amount
    
    peak_spending_day = max(day_spending.items(), key=lambda x: x[1])[0]
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Spending by month
    month_spending = {i: 0 for i in range(1, 13)}
    for expense in expenses:
        expense_date = expense.expense_date
        month_spending[expense_date.month] += expense.amount
    
    peak_spending_month = max(month_spending.items(), key=lambda x: x[1])[0]
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    return {
        "top_categories": top_categories,
        "spending_trend": "stable",  # Could be enhanced with trend analysis
        "peak_spending_day": day_names[peak_spending_day],
        "peak_spending_month": month_names[peak_spending_month - 1],
        "day_spending": {day_names[i]: amount for i, amount in day_spending.items()},
        "month_spending": {month_names[i-1]: amount for i, amount in month_spending.items()}
    }

def get_recent_expenses_summary(expenses: List[Expense], days: int = 7) -> Dict[str, Any]:
    """
    Get summary of recent expenses
    """
    cutoff_date = date.today() - timedelta(days=days)
    recent_expenses = [exp for exp in expenses if exp.expense_date >= cutoff_date]
    
    if not recent_expenses:
        return {
            "count": 0,
            "total_amount": 0,
            "average_amount": 0,
            "categories": []
        }
    
    total_amount = sum(exp.amount for exp in recent_expenses)
    average_amount = total_amount / len(recent_expenses)
    categories = list(set(exp.category for exp in recent_expenses))
    
    return {
        "count": len(recent_expenses),
        "total_amount": total_amount,
        "average_amount": average_amount,
        "categories": categories
    } 