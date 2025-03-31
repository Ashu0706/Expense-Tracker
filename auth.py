from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from requests import Session
import models
from database import get_db
import schema


app = FastAPI()
auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password) 


def verify_password(plain_password, hashed_pasword):
    return pwd_context.verify(plain_password, hashed_pasword)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_router.post("/login/")
def login(credentials : schema.LoginRequest, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password,hash_password("ashutosh123")):
        return "User not found or invalid password"
    else:
        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        return {"access_token": access_token, "user name": user.full_name}


