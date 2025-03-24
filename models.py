

from sqlalchemy import DECIMAL, Column, Date, ForeignKey, Integer, String , Boolean , DateTime, Text , func
from database import Base
from sqlalchemy.orm import relationship

    
    
class Category(Base):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True,primary_key=True)
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Store hashed passwords
    
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_name = Column(String, ForeignKey("categories.name"))
    name = Column(Text, nullable=False)
    amount = Column(DECIMAL(10, 2))
    date = Column(Date)
    description = Column(Text, nullable=True)

    user = relationship("User")
    category = relationship("Category")
    
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_name = Column(String, ForeignKey("categories.name"))
    budget_amount = Column(DECIMAL(10, 2))

    user = relationship("User")
    category = relationship("Category")
    

