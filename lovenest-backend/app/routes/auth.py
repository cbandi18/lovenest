from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.services.db import users_collection
from app.utils.jwt_handler import create_access_token


#Initialize the router
router = APIRouter()

#Setup for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Request Body Schema for signup
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

#--------------------LOGIN API -----------------------------------#

#Request body for login
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(user: LoginRequest):
    try:
        # Step 1: Find the user
        existing_user = users_collection.find_one({"username": user.username})
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Step 2: Check password
        is_valid = pwd_context.verify(user.password, existing_user["password"])
        if not is_valid:
            raise HTTPException(status=401, detail="Invalid username or password")
        
        # Step 3: Generate JWT token
        token = create_access_token(data={"username": user.username})

        # Step 4: Return the token
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException as he:
        return he
    
    except Exception as e:
        print("Login Error: str(e)")
        return HTTPException(status_code=500, detail="Something went wrong.")
