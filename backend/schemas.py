from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    stipend: float = Field(..., gt=0, description="Monthly stipend amount")
    savings_goal: float = Field(..., ge=0, description="Monthly savings goal")
    budget_cycle_start: date = Field(..., description="Start date of budget cycle")

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Expense Schemas
class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount")
    category: str = Field(..., min_length=1, max_length=50, description="Expense category")
    description: Optional[str] = Field(None, max_length=500, description="Expense description")
    expense_date: date = Field(..., alias="date", description="Date of expense")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore"
    }

class ExpenseCreate(ExpenseBase):
    user_id: int = Field(..., description="User ID")

class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Summary Schemas
class BudgetSummary(BaseModel):
    stipend: float
    expenses_by_category: Dict[str, float]
    savings_goal: float
    remaining_budget: float
    daily_limit: float
    total_expenses: float
    days_elapsed: int
    days_remaining: int
    
    class Config:
        from_attributes = True

# Recommendation Schemas
class Recommendation(BaseModel):
    type: str = Field(..., description="Type of recommendation")
    message: str = Field(..., description="Recommendation message")
    priority: str = Field(..., description="Priority level (high/medium/low)")
    
    class Config:
        from_attributes = True

# Report Schemas
class ExpenseReport(BaseModel):
    user_id: int
    expenses: List[Expense]
    total_amount: float
    period_start: date
    period_end: date
    
    class Config:
        from_attributes = True

# API Response Schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None 