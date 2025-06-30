from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv, find_dotenv
import os

from models import Base, engine
from routes import users, expenses, summary
from routes import planned_purchases, advice, deals

# Load environment variables (first look for .env in project root)
load_dotenv(find_dotenv())

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="NYUAD Smart Budgeting Assistant",
    description="A personal budgeting assistant for NYUAD students",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(expenses.router, prefix="/api", tags=["expenses"])
app.include_router(summary.router, prefix="/api", tags=["summary"])
app.include_router(planned_purchases.router, prefix="/api", tags=["planned_purchases"])
app.include_router(advice.router, prefix="/api", tags=["advice"])
app.include_router(deals.router, prefix="/api", tags=["deals"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NYUAD Smart Budgeting Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 