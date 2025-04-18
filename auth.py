from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from requests import Session
import models
from database import get_db
import schema
from fastapi import HTTPException, status


app = FastAPI()
auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password) 


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
      

@auth_router.post("/login")
def login(credential = Depends(OAuth2PasswordRequestForm),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credential.username).first()
    if not user or not verify_password(credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
        
    return {"access_token": access_token, "user name": user.full_name}

    
@auth_router.post("/signin")
def create_user(user: schema.UserCreate, db : Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    
    new_user = models.User(
        username=user.username,
        password=hashed_password,
        full_name=user.full_name,
        email=user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created sucessfully"}

@auth_router.get("/profile")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}

