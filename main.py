import base64
import io
from fastapi import FastAPI,Depends, Response, UploadFile
from requests import Session
from database import get_db
import database
import models
import schema
from sqlalchemy import extract
import fitz
from auth import auth_router
from auth import get_current_user


app = FastAPI()


# Create database tables
models.Base.metadata.create_all(bind=database.engine)


# Include the routes
app.include_router(auth_router)

@app.post("/add_expense/")
async def add_expense(expense : schema.ExpenseCreate,
                      db : Session = Depends(get_db),
                      current_user: schema.User = Depends(get_current_user)):
    
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
                         user_id = current_user.id,
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
async def show_expense(db : Session = Depends(get_db),
                       current_user: schema.User = Depends(get_current_user)):
    
    fetch_exp = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()
    return fetch_exp

@app.get("/categories/")
async def category(db : Session = Depends(get_db),
                   current_user: schema.User = Depends(get_current_user)):
    
    all_category = db.query(models.Category).all()
    return all_category

@app.post("/categories/")
async def category(category : schema.Category,
                   db : Session = Depends(get_db),
                   current_user: schema.User = Depends(get_current_user)):
    
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
    
    
@app.get("/expense/{category}")
async def search_by_category(category, db : Session = Depends(get_db),
                             current_user: schema.User = Depends(get_current_user)):
    
    fetch_category = db.query(
                            models.Expense).filter(models.Expense.category_name == category,
                            models.Expense.user_id == current_user.id).all()
        
    # Extract amounts from the fetched expenses
    amounts = [item.amount for item in fetch_category]

    return {"category": category, "Total Expense": sum(amounts)}

@app.get("/expense/{date}")
async def search_by_category(date, db : Session = Depends(get_db)):
    fetch_date = db.query(models.Expense).filter(models.Expense.date == date).all()
    
    # Extract amounts from the fetched expenses
    amounts = [item.amount for item in fetch_date]

    return {"date": date, "Total Expense": amounts}



@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id : int,
                         db : Session = Depends(get_db),
                         current_user: schema.User = Depends(get_current_user)):
    
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id).first()
    
    if not expense:
        return {"error": "Expense not found"}
    
    # Delete the expense
    db.delete(expense)
    db.commit()
    
    return {"message": "Expense deleted successfully"}


@app.get("/monthly_expenses/{month}")
async def monthly_expense(month : str,
                          db : Session = Depends(get_db),
                          current_user: schema.User = Depends(get_current_user)):
    
    # month dictionary to change user input to int as months sequence
    months_dict = {
    1: 1, "Jan": 1, "jan": 1, "January": 1, "january": 1,
    2: 2, "Feb": 2, "feb": 2, "February": 2, "february": 2,
    3: 3, "Mar": 3, "mar": 3, "March": 3, "march": 3,
    4: 4, "Apr": 4, "apr": 4, "April": 4, "april": 4,
    5: 5, "May": 5, "may": 5,
    6: 6, "Jun": 6, "jun": 6, "June": 6, "june": 6,
    7: 7, "Jul": 7, "jul": 7, "July": 7, "july": 7,
    8: 8, "Aug": 8, "aug": 8, "August": 8, "august": 8,
    9: 9, "Sep": 9, "sep": 9, "September": 9, "september": 9,
    10: 10, "Oct": 10, "oct": 10, "October": 10, "october": 10,
    11: 11, "Nov": 11, "nov": 11, "November": 11, "november": 11,
    12: 12, "Dec": 12, "dec": 12, "December": 12, "december": 12
    }
    
    month = months_dict[month]
    
    # All the expense on particular month
    expense = db.query(models.Expense).filter(
                extract('month', models.Expense.  date) == month,
                models.Expense.user_id == current_user.id).all()
    
    # if no expense 
    if not expense:
        return "Your Expense is 0"
    
    # Total monthly expense
    total_expense_this_month  = sum([item.amount for item in expense])
    
    # All category 
    all_category = [item.category_name for item in expense]
    
    # Stores category wise expense
    category_wise_expense = {}
    for cat in all_category:
        amount = sum([item.amount for item in expense if item.category_name == cat])
        category_wise_expense[cat] = amount
        
    return {
        "Total monthly Expense" : total_expense_this_month ,                "category_wise_expense" : category_wise_expense
        }
    
    
@app.post("/upload/")
async def file_upload(file : UploadFile, db : Session = Depends(get_db)):
    file_content = await file.read()  # Read file content as binary
    new_file = models.FileModel(
                            file_name=file.filename, 
                            file_content=file_content
                            )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return "file uploaded sucessfully"

@app.get("/file/{id}")
async def fetch_file(id : int, db : Session = Depends(get_db)):
    # fetch = db.query(models.FileModel).filter(models.FileModel.file_id == id).all()
    # encoded_image = base64.b64encode(fetch).decode("utf-8")
    # return encoded_image
    image = db.get(models.FileModel, id)
    if not image:
        return {"error": "Image not found"}

    #encoded_image = base64.b64encode(image.file_content).decode("utf-8")
    
    file_stream = io.BytesIO(image.file_content)
    pdf_file = fitz.open(stream=file_stream,filetype="pdf")
    
    return pdf_file
    
    return Response(content=f'<img src="data:image/jpeg;base64,{encoded_image}" />', media_type="text/html")

    

