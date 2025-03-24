from fastapi import FastAPI,Depends
from requests import Session
from database import get_db
import database
import models
import schema

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)


@app.post("/add_expense/")
def add_expense(expense : schema.ExpenseCreate, db : Session = Depends(get_db)):
    # Check if category exists
    category = db.query(models.Category).filter(models.Category.name == expense.category_name).first()
    
    # If category doesn't exist, create it
    if not category:
        category = models.Category(name=expense.category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
        
    # Add expense to table  
    exp = models.Expense(name = expense.name, 
                         amount = expense.amount, 
                        date = expense.date, 
                         description = expense.description, 
                         category_name = expense.category_name
                         )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return {"item added sucessfull": exp}

@app.get("/show_expense/")
def show_expense(db : Session = Depends(get_db)):
    fetch_exp = db.query(models.Expense).all()
    return fetch_exp

@app.get("/categories/")
def category(db : Session = Depends(get_db)):
    all_category = db.query(models.Category).all()
    return all_category

@app.post("/categories/")
def category(category : schema.Category,db : Session = Depends(get_db)):
    # Check if category already exist
    fetch_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    
    #  if not - then add
    if not fetch_category:
        new_category = models.Category(name = category.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return "New category addded Sucessfully"
    else:
        return "Category Already Exist"
    
    
@app.get("/expenses/{category}")
def search_by_category(category, db : Session = Depends(get_db)):
    fetch_category = db.query(models.Expense).filter(models.Expense.category_name == category).all()
    # Extract amounts from the fetched expenses
    amounts = [item.amount for item in fetch_category]

    return {"category": category, "Total Expense": sum(amounts)}

@app.get("/expenses/{date}")
def search_by_category(date, db : Session = Depends(get_db)):
    fetch_date = db.query(models.Expense).filter(models.Expense.date == date).all()
    # Extract amounts from the fetched expenses
    amounts = [item.amount for item in fetch_date]

    return {"date": date, "Total Expense": sum(amounts)}

    