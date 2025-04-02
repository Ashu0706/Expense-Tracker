from datetime import date
from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    user_id: int
    category_name: str
    name : str
    amount: float
    date: date
    description: str | None = None
    
class Category(BaseModel):
    name : str
    
    
class UserCreate(BaseModel):
    username: str
    password: str  
    full_name: str
    email: str
    
    
class User(BaseModel):
    id: str
    username: str
    password: str  
    full_name: str
    email: str
    
    
    


    
    