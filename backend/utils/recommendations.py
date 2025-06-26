from typing import List, Dict, Any
from models import User, Expense
from utils.calculations import calculate_budget_summary, calculate_spending_trends, calculate_savings_progress
from datetime import date, datetime, timedelta

def generate_recommendations(user: User, expenses: List[Expense]) -> List[Dict[str, Any]]:
    """
    Generate personalized financial recommendations based on user's spending patterns
    
    Args:
        user: User object with stipend and savings goal
        expenses: List of user's expenses
    
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    
    if not expenses:
        recommendations.append({
            "type": "welcome",
            "message": "Welcome to NYUAD Budgetly! Start tracking your expenses to get personalized recommendations.",
            "priority": "low"
        })
        return recommendations
    
    # Get budget summary and spending trends
    budget_summary = calculate_budget_summary(user, expenses)
    spending_trends = calculate_spending_trends(expenses)
    savings_progress = calculate_savings_progress(user, expenses)
    
    # Check if over budget
    if budget_summary["remaining_budget"] < 0:
        recommendations.append({
            "type": "over_budget",
            "message": f"You're currently over budget by ${abs(budget_summary['remaining_budget']):.2f}. Consider reducing non-essential expenses.",
            "priority": "high"
        })
    
    # Check savings goal progress
    if not savings_progress["on_track"]:
        deficit = savings_progress["deficit"]
        recommendations.append({
            "type": "savings_goal",
            "message": f"You need to save ${deficit:.2f} more to reach your savings goal. Try cutting back on discretionary spending.",
            "priority": "high"
        })
    
    # Analyze spending by category
    expenses_by_category = budget_summary["expenses_by_category"]
    total_spent = budget_summary["total_expenses"]
    
    # Food spending analysis (recommended: 30% of stipend)
    food_spending = expenses_by_category.get("food", 0)
    food_percentage = (food_spending / user.stipend) * 100 if user.stipend > 0 else 0
    
    if food_percentage > 35:
        recommendations.append({
            "type": "food_spending",
            "message": f"You're spending {food_percentage:.1f}% on food. Consider cooking more meals at home to save money.",
            "priority": "medium"
        })
    
    # Transportation spending analysis (recommended: 15% of stipend)
    transport_spending = expenses_by_category.get("transport", 0) + expenses_by_category.get("transportation", 0)
    transport_percentage = (transport_spending / user.stipend) * 100 if user.stipend > 0 else 0
    
    if transport_percentage > 20:
        recommendations.append({
            "type": "transport_spending",
            "message": f"Transportation costs are {transport_percentage:.1f}% of your budget. Consider using public transport or carpooling.",
            "priority": "medium"
        })
    
    # Entertainment spending analysis (recommended: 10% of stipend)
    entertainment_spending = expenses_by_category.get("entertainment", 0) + expenses_by_category.get("leisure", 0)
    entertainment_percentage = (entertainment_spending / user.stipend) * 100 if user.stipend > 0 else 0
    
    if entertainment_percentage > 15:
        recommendations.append({
            "type": "entertainment_spending",
            "message": f"Entertainment spending is {entertainment_percentage:.1f}% of your budget. Look for free campus activities.",
            "priority": "medium"
        })
    
    # Daily spending analysis
    daily_limit = budget_summary["daily_limit"]
    average_daily = spending_trends["average_daily_spending"]
    
    if average_daily > daily_limit * 1.2:
        recommendations.append({
            "type": "daily_spending",
            "message": f"Your average daily spending (${average_daily:.2f}) is above your daily limit (${daily_limit:.2f}). Try to stay within budget.",
            "priority": "high"
        })
    
    # Positive reinforcement
    if savings_progress["on_track"] and budget_summary["remaining_budget"] > 0:
        recommendations.append({
            "type": "positive",
            "message": "Great job! You're on track with your savings goal and staying within budget. Keep it up!",
            "priority": "low"
        })
    
    # General tips based on spending patterns
    if len(expenses) < 5:
        recommendations.append({
            "type": "tracking",
            "message": "Start tracking all your expenses, even small ones. It helps identify spending patterns.",
            "priority": "low"
        })
    
    # Check for large individual expenses
    largest_expense = max(expense.amount for expense in expenses)
    if largest_expense > user.stipend * 0.1:  # More than 10% of stipend
        recommendations.append({
            "type": "large_expense",
            "message": f"Your largest expense (${largest_expense:.2f}) is significant. Plan for such expenses in advance.",
            "priority": "medium"
        })
    
    # NYUAD-specific recommendations
    recommendations.append({
        "type": "nyuad_tips",
        "message": "Take advantage of NYUAD's free events, gym facilities, and student discounts to save money.",
        "priority": "low"
    })
    
    return recommendations[:5]  # Limit to top 5 recommendations

def get_spending_insights(user: User, expenses: List[Expense]) -> Dict[str, Any]:
    """
    Get detailed spending insights and analysis
    
    Args:
        user: User object
        expenses: List of user's expenses
    
    Returns:
        Dictionary with spending insights
    """
    if not expenses:
        return {
            "insights": ["No expenses recorded yet. Start tracking to get insights!"],
            "patterns": {},
            "suggestions": ["Begin by recording your first expense"]
        }
    
    budget_summary = calculate_budget_summary(user, expenses)
    spending_trends = calculate_spending_trends(expenses)
    
    insights = []
    patterns = {}
    suggestions = []
    
    # Analyze spending patterns
    expenses_by_category = budget_summary["expenses_by_category"]
    
    # Find most expensive category
    if expenses_by_category:
        most_expensive_category = max(expenses_by_category.items(), key=lambda x: x[1])
        insights.append(f"Your highest spending category is {most_expensive_category[0]} (${most_expensive_category[1]:.2f})")
    
    # Analyze daily spending consistency
    daily_spending = spending_trends.get("daily_spending", {})
    if daily_spending:
        spending_variance = max(daily_spending.values()) - min(daily_spending.values())
        if spending_variance > user.stipend * 0.1:
            insights.append("Your daily spending varies significantly. Consider setting daily spending limits.")
    
    # Check for weekend vs weekday spending
    weekend_expenses = [e for e in expenses if e.expense_date.weekday() >= 5]
    weekday_expenses = [e for e in expenses if e.expense_date.weekday() < 5]
    
    if weekend_expenses and weekday_expenses:
        weekend_total = sum(e.amount for e in weekend_expenses)
        weekday_total = sum(e.amount for e in weekday_expenses)
        
        if weekend_total > weekday_total * 1.5:
            insights.append("You spend more on weekends. Consider planning weekend activities with budgets in mind.")
    
    # Generate suggestions
    if budget_summary["remaining_budget"] < user.stipend * 0.2:
        suggestions.append("Set up automatic transfers to savings account")
        suggestions.append("Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings")
    
    if spending_trends["average_daily_spending"] > budget_summary["daily_limit"]:
        suggestions.append("Try the envelope method for discretionary spending")
        suggestions.append("Use cash for daily expenses to feel the spending impact")
    
    return {
        "insights": insights,
        "patterns": {
            "most_expensive_category": max(expenses_by_category.items(), key=lambda x: x[1])[0] if expenses_by_category else None,
            "average_daily_spending": spending_trends["average_daily_spending"],
            "total_expenses": len(expenses)
        },
        "suggestions": suggestions
    }

def analyze_spending_behavior(expenses: List[Expense]) -> Dict[str, Any]:
    """
    Analyze spending behavior patterns
    """
    if not expenses:
        return {
            "behavior_type": "no_data",
            "risk_level": "unknown",
            "habits": []
        }
    
    # Analyze spending frequency
    total_days = len(set(exp.expense_date for exp in expenses))
    total_expenses = len(expenses)
    frequency = total_expenses / max(total_days, 1)
    
    # Analyze expense amounts
    amounts = [exp.amount for exp in expenses]
    avg_amount = sum(amounts) / len(amounts)
    max_amount = max(amounts)
    
    # Determine behavior type
    if frequency > 2:  # More than 2 expenses per day on average
        behavior_type = "frequent_spender"
        risk_level = "medium"
        habits = ["Makes frequent small purchases", "May benefit from batch shopping"]
    elif avg_amount > 100:
        behavior_type = "big_spender"
        risk_level = "high"
        habits = ["Makes large purchases", "Should plan major expenses carefully"]
    elif max_amount > 500:
        behavior_type = "occasional_splurger"
        risk_level = "medium"
        habits = ["Occasionally makes large purchases", "Consider saving for big purchases"]
    else:
        behavior_type = "moderate_spender"
        risk_level = "low"
        habits = ["Balanced spending pattern", "Good foundation for budgeting"]
    
    return {
        "behavior_type": behavior_type,
        "risk_level": risk_level,
        "habits": habits,
        "frequency": frequency,
        "average_amount": avg_amount,
        "max_amount": max_amount
    }

def get_weekend_vs_weekday_analysis(expenses: List[Expense]) -> Dict[str, Any]:
    """
    Compare weekend vs weekday spending patterns
    """
    weekend_expenses = [e for e in expenses if e.expense_date.weekday() >= 5]
    weekday_expenses = [e for e in expenses if e.expense_date.weekday() < 5]
    
    weekend_total = sum(exp.amount for exp in weekend_expenses)
    weekday_total = sum(exp.amount for exp in weekday_expenses)
    
    weekend_avg = weekend_total / len(weekend_expenses) if weekend_expenses else 0
    weekday_avg = weekday_total / len(weekday_expenses) if weekday_expenses else 0
    
    return {
        "weekend_total": weekend_total,
        "weekday_total": weekday_total,
        "weekend_avg": weekend_avg,
        "weekday_avg": weekday_avg,
        "weekend_count": len(weekend_expenses),
        "weekday_count": len(weekday_expenses),
        "spends_more_on_weekends": weekend_avg > weekday_avg
    } 