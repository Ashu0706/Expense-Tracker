

from sqlalchemy import DECIMAL, Column, Date, ForeignKey, Integer, LargeBinary, String , Boolean , DateTime, Text , func
from database import Base
from sqlalchemy.orm import relationship

    
    
class Category(Base):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True,primary_key=True)
    
    
class User(Base):
    __tablename__ = "user"
    
    username = Column(String, primary_key=True)
    password = Column(String)
    full_name = Column(String)
    email = Column(String)
    
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.username"))
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
    user_id = Column(Integer, ForeignKey("user.username"))
    category_name = Column(String, ForeignKey("categories.name"))
    budget_amount = Column(DECIMAL(10, 2))

    user = relationship("User")
    category = relationship("Category")
    
class FileModel(Base):
    __tablename__ = "file"
    
    file_id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_content = Column(LargeBinary)
    


