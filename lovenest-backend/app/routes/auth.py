from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.services.db import users_collection

from fastapi import Depends


#Initialize the router
router = APIRouter()

#Setup for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Request Body Schema
class SignupRequest(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

#API endpoint for user signup
@router.post("/signup")
def signup(user: SignupRequest):
    #Check if user already exists
    try:
    # DEBUG: Check if username already exists
        existing_user = users_collection.find_one({"username": user.username})
        print("Existing user check result:", existing_user)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        #Hash the password
        hashed_pwd = pwd_context.hash(user.password)

        #Build your document
        new_user = {
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "password": hashed_pwd
        }

        #Save these user details to MONGODB
        users_collection.insert_one(new_user)

        return {"Message": "User registered successfully"}
    
    except HTTPException as he: 
        # Do not block or overwrite FastAPI's expected HTTP exceptions
        raise he
    
    except Exception as e:
        print("ERROR in signup:", str(e))
        raise HTTPException(status_code=500, detail="Something went wrong.")