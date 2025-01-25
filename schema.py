from datetime import datetime
from pydantic import BaseModel, validator

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True

# Expense Schemas
class ExpenseBase(BaseModel):
    description: str
    amount: float  # User input in currency units
    category: str
    expense_date: datetime

class ExpenseCreate(ExpenseBase):
    @validator('amount')
    def convert_to_cents(cls, v):
        return int(round(v * 100))  # Store as cents

class ExpenseResponse(ExpenseBase):
    id: int
    amount: float  # Return as currency units
    time_created: datetime
    time_updated: datetime
    user_id: int

    @validator('amount', pre=True)
    def convert_from_cents(cls, v):
        return v / 100  # Convert from cents

    class Config:
        orm_mode = True

# Authentication Schema
class LoginRequest(BaseModel):
    username: str
    password: str