import os
from datetime import datetime, timedelta

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import User, Expense
from schema import (UserCreate, UserResponse, ExpenseCreate,
                    ExpenseResponse, LoginRequest, Token)

load_dotenv(".env")

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# JWT Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.session.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user

@app.post("/register/", response_model=UserResponse)
def register(user: UserCreate):
    # Check if username or email exists
    existing_user = db.session.query(User).filter(
        (User.username == user.username) | 
        (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
        
    new_user = User(
        username=user.username,
        email=user.email
    )
    new_user.set_password(user.password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

@app.post("/login/", response_model=Token)
def login(login_data: LoginRequest):
    user = db.session.query(User).filter(
        User.username == login_data.username
    ).first()
    
    if not user or not user.check_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserResponse)
def get_current_user_details(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/expenses/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user)
):
    db_expense = Expense(
        **expense.dict(),
        user_id=current_user.id
    )
    db.session.add(db_expense)
    db.session.commit()
    return db_expense

@app.get("/expenses/", response_model=list[ExpenseResponse])
def get_user_expenses(current_user: User = Depends(get_current_user)):
    return db.session.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

@app.get("/")
def root():
    return {"message": "Expense Tracker API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)