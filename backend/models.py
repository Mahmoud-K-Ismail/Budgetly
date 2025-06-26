from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./budgetly.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User model for storing student profile information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    stipend = Column(Float, nullable=False, comment="Monthly stipend amount")
    savings_goal = Column(Float, nullable=False, default=0.0, comment="Monthly savings goal")
    budget_cycle_start = Column(Date, nullable=False, comment="Start date of budget cycle")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with expenses
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, stipend={self.stipend}, savings_goal={self.savings_goal})>"

class Expense(Base):
    """Expense model for storing individual expense records"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False, comment="Expense amount")
    category = Column(String(50), nullable=False, comment="Expense category")
    description = Column(Text, nullable=True, comment="Expense description")
    expense_date = Column(Date, nullable=False, comment="Date of expense")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = relationship("User", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category={self.category})>"

# Database dependency
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 